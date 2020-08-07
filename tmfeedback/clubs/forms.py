from django import forms

from .models import Club


class MembershipRequestForm(forms.Form):
    pass


class MembershipApprovalForm(forms.Form):
    CHOICES = [('Y', 'Approve'), ('N', 'Deny')]
    request_decision = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect)


def create_membership_request_formset(form_count):
    return forms.formset_factory(MembershipApprovalForm, extra=form_count)


class ClubModelForm(forms.ModelForm):
    class Meta:
        model = Club
        fields = ['name', 'id', 'description']
