from . import factories
from biz_content import models, forms
from django.test import TestCase
from django.core.urlresolvers import reverse


class CheckListFormTestCase(TestCase):
    def setUp(self):
        self.project = factories.ProjectFactory()
        self.step_page = factories.StepPageFactory()

    def test_init_without_project(self):
        form = forms.ChecklistForm(self.step_page)
        print(form)
