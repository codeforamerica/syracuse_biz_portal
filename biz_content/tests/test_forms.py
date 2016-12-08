from . import factories
from biz_content import models, forms
from django.test import TransactionTestCase, TestCase
from django.core.urlresolvers import reverse


class CheckListFormTestCase(TestCase):
    def setUp(self):
        self.project = factories.ProjectFactory()
        self.step_page = factories.StepPageFactory()

    def test_init_without_project(self):
        form = forms.ChecklistForm(self.step_page)
        cl = form.fields['checklist']
        form_qs = list(cl._queryset.values_list('pk', flat=True))
        qs = list(self.step_page.checklist_items.values_list('pk', flat=True))
        self.assertListEqual(form_qs, qs)

