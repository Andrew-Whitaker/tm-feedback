from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView

from .models import Meeting
from clubs.models import Club


class MeetingIndex(ListView):
    model = Meeting
    paginate_by = 20
    context_object_name = 'meetings'
    template_name = 'meetings/simple_meeting_index.html'

    def get_queryset(self):
        self.club = get_object_or_404(Club, pk=self.kwargs.get('club_id'))
        queryset = self.club.meetings.order_by('date')
        return queryset

    def get_context_data(self, **kwargs):
        kwargs['club'] = self.club
        return super().get_context_data(**kwargs)

