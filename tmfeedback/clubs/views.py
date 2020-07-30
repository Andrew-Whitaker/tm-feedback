
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, View
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
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


class ClubManageRequestsView(LoginRequiredMixin, View):

    def get(self, request, club_id):
        club = get_object_or_404(Club, pk=club_id)
        requesters = get_user_model().objects.filter(pending_clubs__pk=club_id)
        request_count = requesters.count()
        formset = create_membership_request_formset(request_count)()

        request_forms = zip(formset, requesters)
        context = {'form_requests': request_forms,
                   'club': club,
                   'formset': formset,
                   'request_count': request_count
                   }
        return render(request, 'clubs/club_manage_requests.html', context)

    def post(self, request, club_id, **kwargs):
        club = get_object_or_404(Club, pk=club_id)
        requesters = get_user_model().objects.filter(pending_clubs__pk=club_id)
        request_count = requesters.count()
        formset = create_membership_request_formset(request_count)(request.POST)

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
        # request_count = int(request.context['request_count'])
        #
        # formset = create_membership_request_formset(request_count)(request.POST)
        # for
        #     clean_data = formset.cle
        #






