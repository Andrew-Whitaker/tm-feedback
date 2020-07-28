
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, View
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
import sys

from .models import Club
from .forms import MembershipRequestForm


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

# class ClubOrganizer


