from . import factories
from biz_content import models, forms
from django.contrib.auth.models import AnonymousUser
from django.test import TransactionTestCase, TestCase
from django.test.client import RequestFactory


class StepPageTestCase(TransactionTestCase):

    def setUp(self):
        self.project = factories.ProjectFactory()
        self.step_page = factories.StepPageFactory()
        self.rf = RequestFactory()

    def test_get_context_without_project(self):
        request = self.rf.get('/')
        request.user = AnonymousUser()
        context = self.step_page.get_context(request)
        self.assertTrue('checklists' in context)
        checklists = context['checklists']
        self.assertEqual(len(checklists), 1)
        self.assertTrue(isinstance(checklists[0], forms.ChecklistForm))
        self.assertIsNone(checklists[0].project)

    def test_get_context_with_project(self):
        request = self.rf.get('/')
        request.user = self.project.owner
        context = self.step_page.get_context(request)
        self.assertTrue('checklists' in context)
        checklists = context['checklists']
        self.assertEqual(len(checklists), 1)
        self.assertTrue(isinstance(checklists[0], forms.ChecklistForm))
        self.assertEqual(checklists[0].project, self.project)
