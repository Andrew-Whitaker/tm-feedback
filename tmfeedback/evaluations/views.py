from django.shortcuts import render, get_object_or_404
from django.contrib.auth import get_user_model
from django.views.generic import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from .models import Evaluation
from .forms import EvalCreationForm
from clubs.models import Club
from meetings.models import Meeting, Performance


class ClubMembershipRequiredMixin(UserPassesTestMixin):
    """ Mixin that enforces the request's user be a member of a particular club.
    This mixin assumes that:
        1) kwargs is a member variable of self
        2) the key 'perf_pk' exists in kwargs
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
        performance = get_object_or_404(Performance, pk=self.kwargs['perf_pk'])
        return performance.meeting.club


class EvalCreateView(LoginRequiredMixin, ClubMembershipRequiredMixin, CreateView):
    template_name = 'evaluations/eval_create.html'
    form_class = EvalCreationForm

    def form_valid(self, form):
        perf_pk = self.kwargs.get('perf_pk')
        form.instance.performance = get_object_or_404(Performance, pk=perf_pk)
        form.instance.evaluator = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        perf_pk = self.kwargs.get('perf_pk')
        perf = get_object_or_404(Performance, pk=perf_pk)
        meeting = perf.meeting
        club = meeting.club
        context = super().get_context_data(**kwargs)
        context['club'] = club
        context['meeting'] = meeting
        context['performance'] = perf
        return context

