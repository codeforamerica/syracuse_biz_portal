from . import factories
from biz_content import models, forms
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.http import QueryDict
from django.test import TestCase, TestCase
from django.test.client import RequestFactory
from django.core.exceptions import ValidationError


class FormValidationTestCase(TestCase):

    def setUp(self):
        self.cu_id = 'CU-123-234'
        self.bad_cu_id = '123-234'
        self.bad_character_cu_id = 'CU!!!2132'

    def test_validate_cu(self):
        """Checkbox items and form items should match"""
        with self.assertRaises(forms.ValidationError):
            forms.starts_with_cu(
                self.bad_cu_id)

    def test_validate_is_letter_number_dashes(self):
        with self.assertRaises(forms.ValidationError):
            forms.is_letter_number_dashes(
                self.bad_character_cu_id)

    def test_validate_pc(self):
        with self.assertRaises(forms.ValidationError):
            forms.starts_with_pc(
                self.bad_character_cu_id)
