from django import forms
from django.forms.widgets import SelectDateWidget

from .models import Evaluation


class EvalCreationForm(forms.ModelForm):

    class Meta:
        model = Evaluation
        fields = ['you_excelled_at', 'to_work_on', 'challenge_yourself_by']

