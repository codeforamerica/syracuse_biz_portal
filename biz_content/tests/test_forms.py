from . import factories
from biz_content import models, forms
from django.test import TransactionTestCase, TestCase
from django.core.urlresolvers import reverse


class CheckListFormTestCase(TransactionTestCase):
    def setUp(self):
        self.project = factories.ProjectFactory()
        self.step_page = factories.StepPageFactory()

    def test_init_without_project(self):
        form = forms.ChecklistForm(self.step_page)
        cl = form.fields['checklist']
        form_qs = cl._queryset.values('pk')
        qs = self.step_page.checklist_items.values('pk')
        self.assertQuerysetEqual(form_qs, map(str,qs))

