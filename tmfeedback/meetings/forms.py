from django import forms
from django.forms.widgets import SelectDateWidget

from .models import Meeting


class MeetingCreationForm(forms.ModelForm):
    date = forms.DateField(
        widget=SelectDateWidget(
            empty_label=('Choose Month', 'Choose Day', 'Choose Year')
        )
    )

    class Meta:
        model = Meeting
        exclude = ('club',)




