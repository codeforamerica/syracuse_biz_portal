from . import factories
from biz_content import models
from django.contrib.auth.models import AnonymousUser
from django.test import TransactionTestCase, TestCase
from django.test.client import RequestFactory


class StepPageTestCase(TestCase):

    def setUp(self):
        self.user = factories.UserFactory()
        self.step_page = factories.StepPageFactory()
        self.rf = RequestFactory()

    """
    TODO: Needs tests for prev and next step page
    """
