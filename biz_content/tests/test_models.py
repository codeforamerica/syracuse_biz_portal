from . import factories
from biz_content import models, forms
from django.contrib.auth.models import AnonymousUser
from django.test import TransactionTestCase, TestCase
from django.test.client import RequestFactory


class StepPageTestCase(TestCase):

    def setUp(self):
        self.user = factories.UserFactory()
        self.step_page = factories.StepPageFactory()
        self.rf = RequestFactory()

    def test_get_context_without_project(self):
        request = self.rf.get('/')
        context = self.step_page.get_context(request)
        self.assertTrue('checklists' in context)
        checklists = context['checklists']
        self.assertEqual(len(checklists), 1)
        self.assertTrue(isinstance(checklists[0], forms.ChecklistForm))
