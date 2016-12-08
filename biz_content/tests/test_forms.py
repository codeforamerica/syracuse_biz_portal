from . import factories
from biz_content import models, forms
from django.test import TransactionTestCase
from django.core.urlresolvers import reverse


class CheckListFormTestCase(TransactionTestCase):
    def setUp(self):
        self.project = factories.ProjectFactory()
        self.step_page = factories.StepPageFactory()

    def test_init_without_project(self):
        form = forms.ChecklistForm(self.step_page)
        cl = form.fields['checklist']
        form_qs = cl._queryset.all()
        qs = self.step_page.checklist_items
        self.assertQuerysetEqual(form_qs, qs)

