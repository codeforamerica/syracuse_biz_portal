from . import factories
from biz_content import models, forms
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.http import QueryDict
from django.test import TransactionTestCase, TestCase
from django.test.client import RequestFactory


class ChecklistFormTestCase(TransactionTestCase):

    def setUp(self):
        self.user = factories.UserFactory()
        self.project = self.user.projects.all()[0]
        self.step_page = factories.StepPageFactory()

    def test_init_without_project(self):
        """Checkbox items and form items should match"""
        form = forms.ChecklistForm(self.step_page)
        cl = form.fields['checklist']
        form_qs = cl._queryset.values('pk')
        qs = self.step_page.checklist_items.values('pk')
        self.assertQuerysetEqual(qs, form_qs, transform=lambda x: x)

    def test_init_with_project(self):
        form = forms.ChecklistForm(self.step_page, project=self.project)
        cl = form.fields['checklist']
        form_qs = cl._queryset.values('pk')
        qs = self.step_page.checklist_items.values('pk')
        self.assertQuerysetEqual(qs, form_qs, transform=lambda x: x)
        model_items = self.project.checked_items.values('pk')
        form_items = cl.initial
        self.assertQuerysetEqual(model_items, form_items,
                                 transform=lambda x: x)

    def test_add_checklist_without_checked_items(self):
        rf = RequestFactory()
        request = rf.post('/', {})
        request.user = self.user
        request._dont_enforce_csrf_check = False
        form = forms.ChecklistForm(self.step_page, request.POST,
                                   project=self.project)
        self.assertTrue(form.is_valid())
        form.save()
        self.assertEqual(self.project.checklists.count(), 1)

    def test_cleaned_data(self):
        rf = RequestFactory()
        items = self.step_page.checklist_items.all()
        query = {'checklist': tuple(items.values_list('pk', flat=True))}
        request = rf.post('/', query)
        request.user = self.user
        request._dont_enforce_csrf_check = False
        form = forms.ChecklistForm(self.step_page, request.POST,
                                   project=self.project)
        self.assertTrue(form.is_valid())
        checked_items = form.cleaned_data['checklist']
        self.assertEquals(checked_items.count(), items.count())

    def test_add_checklist_with_checked_items(self):
        rf = RequestFactory()
        items = self.step_page.checklist_items.all()
        query = {'checklist': tuple(items.values_list('pk', flat=True))}
        request = rf.post('/', query)
        request.user = self.user
        request._dont_enforce_csrf_check = False
        form = forms.ChecklistForm(self.step_page, request.POST,
                                   project=self.project)
        self.assertTrue(form.is_valid())
        form.save()
        self.assertEqual(self.project.checklists.count(), 1)
        self.assertEqual(self.project.checked_items.count(), items.count())


class UserFormTestCase(TransactionTestCase):

    def setUp(self):
        self.email = 'test@gmail.com'
        self.password = 'knew1for!'

    def test_create_user(self):
        """Checkbox items and form items should match"""

        initial_data = {'email': self.email,
                        'password1': self.password,
                        'password2': self.password}

        form = forms.CustomUserCreationForm(initial_data)
        self.assertTrue(form.is_valid())
        form.save()
        u = User.objects.get(email=self.email)
        self.assertEqual(u.username, self.email)
