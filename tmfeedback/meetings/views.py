from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, CreateView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
import sys

from .models import Meeting
# from .forms import MeetingCreationForm
from clubs.models import Club
from clubs.views import ClubMemberPermissionRequiredMixin, ClubOrganizerPermissionRequiredMixin


class MeetingListView(ListView):
    model = Meeting
    paginate_by = 20
    context_object_name = 'meetings'
    template_name = 'meetings/meeting_list.html'

    def get_queryset(self):
        self.club = get_object_or_404(Club, pk=self.kwargs.get('club_id'))
        queryset = self.club.meetings.order_by('date')
        return queryset

    def get_context_data(self, **kwargs):
        kwargs['club'] = self.club
        return super().get_context_data(**kwargs)


class MeetingDetailView(DetailView):
    template_name = 'meetings/meeting_detail.html'
    context_object_name = 'meeting'

    def get_object(self):
        meeting_pk = self.kwargs.get('meeting_pk')
        return get_object_or_404(Meeting, pk=meeting_pk)

    def get_context_data(self, **kwargs):
        club_id = self.kwargs.get('club_id')
        context = super().get_context_data(**kwargs)
        context['club'] = get_object_or_404(Club, id=club_id)
        return context

# class NewMeetingView(LoginRequiredMixin, ClubMemberPermissionRequiredMixin, CreateView):
#     template_name = 'meetings/new_meeting.html'
#     # TODO: specify a form_class to add extra validation so that clubs can't have multiple meetings with the same date
#     # form_class = MeetingCreationForm
#
#     def get_initial(self, *args, **kwargs):
#         initial = super(NewMeetingView, self).get_initial(**kwargs)
#         initial['theme'] = 'Meeting Theme'
#         return initial
#
#     def form_valid(self, form):


