from . import factories
from biz_content import models, forms
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.http import QueryDict
from django.test import TestCase, TestCase
from django.test.client import RequestFactory


class BizLicenseFormTestCase(TestCase):

    def setUp(self):
        self.cu_id = 'CU-123-234'
        self.bad_cu_id = '123-234'

    def test_form_validates_cu(self):
        """Checkbox items and form items should match"""
        initial_data = {'cu_id': self.cu_id}
        form = forms.BizLicenseStatusForm(initial_data)
        self.assertTrue(form.is_valid())

    def test_form_raises_error_without_cu(self):
        initial_data = {'cu_id': self.bad_cu_id}
        form = forms.BizLicenseStatusForm(initial_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors['cu_id'][0],
            "Your business license identifier must start with CU")
