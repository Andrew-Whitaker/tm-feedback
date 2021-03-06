
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, View, FormView, DetailView, TemplateView
from django.views.generic.list import MultipleObjectMixin
from django.views.generic.detail import SingleObjectMixin
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.forms import formset_factory
import sys
from datetime import date

from .models import Club
from .forms import MembershipRequestForm, MembershipApprovalForm, create_membership_request_formset, ClubModelForm


class ClubOrganizerRequiredMixin(UserPassesTestMixin):
    """ Mixin that enforces the request's user be the organizer for a particular club.
    This mixin assumes that:
        1) kwargs is a member variable of self
        2) the key 'club_id' exists in kwargs
        3) request is a member variable of self
    Should always be used after LoginRequiredMixin.
    """
    def test_func(self):
        club = self.get_club()
        user = self.request.user
        return Club.objects.filter(id=club.id, organizer=user).exists()

    def get_club(self):
        return get_object_or_404(Club, pk=self.kwargs['club_id'])


class ClubMembershipRequiredMixin(UserPassesTestMixin):
    """ Mixin that enforces the request's user be the organizer for a particular club.
    This mixin assumes that:
        1) kwargs is a member variable of self
        2) the key 'club_id' exists in kwargs
        3) request is a member variable of self
    Should always be used after LoginRequiredMixin.

    Can override get_club method to use this mixin for views that do not have 'club_id'
    in its kwargs. Allows extendability for any circumstance in which a club can be found.
    """
    def test_func(self):
        club = self.get_club()
        user = self.request.user
        return club.has_member(user)

    def get_club(self):
        return get_object_or_404(Club, pk=self.kwargs['club_id'])


class ClubIndexView(ListView):
    model = Club
    context_object_name = 'clubs'
    template_name = 'clubs/club_index.html'


class ClubHomeView(View):
    @staticmethod
    def get(request, club_id):
        club = get_object_or_404(Club, pk=club_id)
        user = request.user
        context = {
            'club': club,
            'meetings': club.get_meetings_from_last_n_weeks(6),
            'members': club.get_roster()
        }
        if user.is_authenticated:
            context['is_member'] = club.has_member(user)
            context['has_pending_membership'] = club.has_pending_member(user)
        else:
            context['is_member'] = False
            context['is_member'] = False

        return render(request, 'clubs/club_home.html', context)

    def post(self, request, club_id):
        form = MembershipRequestForm(request.POST)
        if form.is_valid():
            user = request.user
            club = get_object_or_404(Club, pk=club_id)
            club.membership_requests.add(user)
            club.save()
            return redirect('clubs:home', club_id=club_id)
        else:
            return redirect('clubs:index')


class ClubCreateView(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        view = ClubCreationDisplay.as_view()
        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        view = ClubCreationSubmission.as_view()
        return view(request, *args, **kwargs)


class ClubCreationDisplay(TemplateView):
    template_name = 'clubs/club_create.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = ClubModelForm()
        return context


class ClubCreationSubmission(TemplateView):
    template_name = 'clubs/club_create.html'

    def post(self, request):
        form = ClubModelForm(request.POST)
        if form.is_valid():
            new_club = form.save(commit=False)
            new_club.organizer = request.user
            new_club.save()
            new_club.add_member(request.user)
            return redirect('clubs:home', club_id=new_club.id)
        else:
            return render(request, 'clubs/club_create.html', {'form': form})


class ClubMemberRoster(LoginRequiredMixin, ListView):
    login_url = '/login/'
    model = get_user_model()
    context_object_name = 'members'
    template_name = 'clubs/club_member_roster.html'
    paginate_by = 20

    def get_context_data(self, **kwargs):
        kwargs['club'] = self.club
        return super().get_context_data(**kwargs)

    def get_queryset(self):
        self.club = get_object_or_404(Club, id=self.kwargs.get('club_id'))
        queryset = self.club.members.order_by('-last_name')
        return queryset


class ClubManageRequestsView(LoginRequiredMixin, ClubOrganizerRequiredMixin, View):

    def get(self, request, club_id):
        club = get_object_or_404(Club, pk=club_id)
        requesters = get_user_model().objects.filter(pending_clubs__pk=club_id)
        requesters = requesters.order_by('first_name')
        formset = create_membership_request_formset(requesters.count())()

        request_forms = zip(formset, requesters)
        context = {'form_requests': request_forms,
                   'club': club,
                   'formset': formset,
                   'request_count': requesters.count()
                   }
        return render(request, 'clubs/club_membership_requests.html', context)

    def post(self, request, club_id):
        club = get_object_or_404(Club, pk=club_id)
        requesters = get_user_model().objects.filter(pending_clubs__pk=club_id)
        requesters = requesters.order_by('first_name')
        formset = create_membership_request_formset(requesters.count())(request.POST)

        for form, user in zip(formset, requesters):
            if form.is_valid():
                data = form.cleaned_data
                self.fulfill_membership_decision(data, user, club)

        return redirect('clubs:member_roster', club_id=club_id)

    @staticmethod
    def fulfill_membership_decision(form_data, user, club):
        response_key = 'request_decision'
        if response_key in form_data.keys():
            if form_data[response_key] == 'Y':
                club.membership_requests.remove(user)
                club.members.add(user)
                club.save()
            else:
                club.membership_requests.remove(user)
                club.save()
        return


# class ClubMembershipRequestDisplay(LoginRequiredMixin, ClubOrganizerPermissionRequiredMixin, DetailView):
#     model = Club
#     pk_url_kwarg = 'club_id'
#     context_object_name = 'club'
#     template_name = 'clubs/club_membership_requests.html'
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#
#         requesters = self.object.membership_requests.all()
#         requesters = requesters.order_by('first_name')
#         formset = create_membership_request_formset(requesters.count())()
#
#         context['formset'] = formset
#         context['form_requests'] = zip(formset, requesters)
#
#         return context
#
#
# class ClubMembershipRequestApproval(LoginRequiredMixin,
#         ClubOrganizerPermissionRequiredMixin, SingleObjectMixin, FormView):
#     form_class = create_membership_request_formset(1)
#     model = Club
#     pk_url_kwarg = 'club_id'
#     context_object_name = 'club'
#     template_name = 'clubs/club_membership_requests.html'
#
#     def post(self, request, *args, **kwargs):
#
#
#         return super().post(request, *args, **kwargs)
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#
#         requesters = self.object.membership_requests.all()
#         requesters = requesters.order_by('first_name')
#         formset = create_membership_request_formset(requesters.count())(self.request.POST)
#
#         context['formset'] = formset
#         context['form_requests'] = zip(formset, requesters)
#
#         return context
#
#     def get_success_url(self):
#
# class ClubManageMembershipRequests(LoginRequiredMixin, View):
#
#     def get(self, request, *args, **kwargs):
#         view = ClubMembershipRequestDisplay.as_view()
#         return view(request, *args, **kwargs)
#
#     def post(self, request, *args, **kwargs):
#         view = ClubMembershipRequestApproval.as_view()
#         return view(request, *args, **kwargs)



