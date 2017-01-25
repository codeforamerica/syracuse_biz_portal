from django import forms
from django.db import transaction
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class ChecklistForm(forms.Form):

    def __init__(self, steppage, *args, **kwargs):
        self.step_page = steppage
        super().__init__(*args, **kwargs)
        items = self.step_page.checklist_items
        self.fields['checklist'] = forms.ModelMultipleChoiceField(
            queryset=items, required=False,
            widget=forms.CheckboxSelectMultiple)


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('email', 'password1', 'password2')

    def save(self, commit=True):
        user = super(CustomUserCreationForm, self).save(commit=False)
        user.username = user.email

        if commit:
            user.save()

        return user


class PermitStatusForm(forms.Form):
    permit_id = forms.CharField(required=True,
                                label="Permit ID",
                                help_text="Enter your Permit Application ID")
