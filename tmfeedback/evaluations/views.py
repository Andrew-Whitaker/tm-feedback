from django.shortcuts import render, get_object_or_404
from django.contrib.auth import get_user_model
from django.views.generic import CreateView

from .models import Evaluation
from .forms import EvalCreationForm
from clubs.models import Club
from meetings.models import Meeting, Performance


class EvalCreateView(CreateView):
    template_name = 'evaluations/eval_create.html'
    form_class = EvalCreationForm

    def form_valid(self, form):
        perf_pk = self.kwargs.get('perf_pk')
        form.instance.performance = get_object_or_404(Performance, pk=perf_pk)
        form.instance.evaluator = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        club_id = self.kwargs.get('club_id')
        meeting_pk = self.kwargs.get('meeting_pk')
        perf_pk = self.kwargs.get('perf_pk')
        context = super().get_context_data(**kwargs)
        context['club'] = get_object_or_404(Club, id=club_id)
        context['meeting'] = get_object_or_404(Meeting, pk=meeting_pk)
        context['performance'] = get_object_or_404(Performance, pk=perf_pk)
        return context
