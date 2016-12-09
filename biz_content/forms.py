from django import forms


class ChecklistForm(forms.Form):

    def __init__(self, steppage, *args, **kwargs):
        self.step_page = steppage
        self.project = kwargs.pop('project', None)
        super().__init__(*args, **kwargs)
        items = self.step_page.checklist_items
        self.fields['checklist'] = forms.ModelMultipleChoiceField(
            queryset=items)
        if self.project:
            pks = set(items.values_list('pk', flat=True))
            checked_items = self.project.checked_items
            checked_pks = set(checked_items.values_list('pk', flat=True))
            checked_pks.intersection(pksx)
            self.fields['checklist'].initial = checked_items.values('pk')
