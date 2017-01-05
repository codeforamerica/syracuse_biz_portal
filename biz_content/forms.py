from django import forms
from django.db import transaction
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class ChecklistForm(forms.Form):

    def __init__(self, steppage, *args, **kwargs):
        self.step_page = steppage
        self.project = kwargs.pop('project', None)
        super().__init__(*args, **kwargs)
        items = self.step_page.checklist_items
        self.fields['checklist'] = forms.ModelMultipleChoiceField(
            queryset=items, required=False,
            widget=forms.CheckboxSelectMultiple)
        if self.project:
            pks = set(items.values_list('pk', flat=True))
            checked_items = self.project.checked_items
            checked_pks = set(checked_items.values_list('pk', flat=True))
            project_checked_pks = checked_pks.intersection(pks)
            self.fields['checklist'].initial = project_checked_pks

    def save(self):
        try:
            self.project.checklists.get(pk=self.step_page.pk)
        except ObjectDoesNotExist:
            self.project.checklists.add(self.step_page)
        with transaction.atomic():
            self.project.checked_items.filter(
                checklist=self.step_page).delete()
            for item in self.cleaned_data['checklist']:
                self.project.checked_items.add(item)
        return self.project.checked_items


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
