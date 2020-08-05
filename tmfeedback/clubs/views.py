
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, View, FormView, DetailView
from django.views.generic.list import MultipleObjectMixin
from django.views.generic.detail import SingleObjectMixin
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.forms import formset_factory
import sys

from .models import Club
from .forms import MembershipRequestForm, MembershipApprovalForm, create_membership_request_formset


class ClubIndexView(ListView):
    model = Club
    context_object_name = 'clubs'
    template_name = 'clubs/club_index.html'


class ClubHomeView(View):
    @staticmethod
    def get(request, club_id):
        club = get_object_or_404(Club, pk=club_id)
        user = request.user
        if user.is_authenticated:
            context = {
                'club': club,
                'is_member': club.has_member(user),
                'has_pending_membership': club.has_pending_member(user)
            }
            return render(request, 'clubs/club_home.html', context)
        else:
            context = {
                'club': club,
                'is_member': False,
                'has_pending_membership': False
            }
            return render(request, 'clubs/club_home.html', context)

    def post(self, request, club_id):
        form = MembershipRequestForm(request.POST)
        if form.is_valid():
            user = request.user
            club = get_object_or_404(Club, pk=club_id)
            club.membership_requests.add(user)
            club.save()
            return redirect('club_home', club_id=club_id)
        else:
            return redirect('club_index')


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


class ClubOrganizerPermissionRequiredMixin(UserPassesTestMixin):
    """ Mixin that enforces the request's user be the organizer for a particular club.
    This mixin assumes that:
        1) kwargs is a member variable of self
        2) the key 'club_id' exists in kwargs
        3) request is a member variable of self
    Should always be used after LoginRequiredMixin.
    """
    def test_func(self):
        club = get_object_or_404(Club, pk=self.kwargs['club_id'])
        user = self.request.user
        return Club.objects.filter(id=club.id, organizer=user).exists()


class ClubMemberPermissionRequiredMixin(UserPassesTestMixin):
    """ Mixin that enforces the request's user be the organizer for a particular club.
    This mixin assumes that:
        1) kwargs is a member variable of self
        2) the key 'club_id' exists in kwargs
        3) request is a member variable of self
    Should always be used after LoginRequiredMixin.
    """
    def test_func(self):
        club = get_object_or_404(Club, pk=self.kwargs['club_id'])
        user = self.request.user
        return club.has_member(user)


class ClubManageRequestsView(LoginRequiredMixin, ClubOrganizerPermissionRequiredMixin, View):

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

        return redirect('club_member_roster', club_id=club_id)

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



