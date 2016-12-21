from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class ChecklistForm(forms.Form):

    def __init__(self, steppage, *args, **kwargs):
        self.step_page = steppage
        self.project = kwargs.pop('project', None)
        super().__init__(*args, **kwargs)
        items = self.step_page.checklist_items
        self.fields['checklist'] = forms.ModelMultipleChoiceField(
            queryset=items, widget=forms.CheckboxSelectMultiple)
        if self.project:
            pks = set(items.values_list('pk', flat=True))
            checked_items = self.project.checked_items
            checked_pks = set(checked_items.values_list('pk', flat=True))
            checked_pks.intersection(pks)
            self.fields['checklist'].initial = checked_items.values('pk')


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('email', 'password1', 'password2')

    def save(self, commit=True):
        user = super(CustomUserCreationForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        user.username = user.email

        if commit:
            user.save()

        return user
