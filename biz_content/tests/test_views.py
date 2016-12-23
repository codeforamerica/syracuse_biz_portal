from . import factories
from biz_content import models, forms
from django.test import TestCase
from django.core.urlresolvers import reverse
from django.contrib.auth.models import Permission
from mock import patch


class ProfileViewTestCase(TestCase):

    def setUp(self):
        """Set Up User
        Set up user with permissions to access admin."""
        self.user = factories.UserFactory()
        self.user.save()
        self.steppage = factories.StepPageFactory()
        self.steppage.save()
        self.project = self.user.projects.first()
        self.project.checklists.add(self.steppage)


    def test_view_redirects_to_login(self):
        """Profile redirect to login if not logged in.
        """
        res = self.client.get(reverse('profile'))
        expected_redirect = "%s?next=%s" % (
            reverse('auth_login'), reverse('profile'))

        self.assertRedirects(res, expected_redirect)

    def test_auth_user_logs_in(self):
        """User goes to profile if logged in.
        """
        self.client.force_login(self.user)
        res = self.client.get(reverse('profile'))
        self.assertEquals(res.status_code, 200)

#    @patch('biz_content.views.foo')
#    def test_project_checklists(self, mock_render):
#        """Test project checklist.
#        """

#        self.client.force_login(self.user)
#        res = self.client.get(reverse('profile'))
#        called_with = mock_render.call_args
#        checklists = called_with[2]['checklists']
#        self.assertEquals(checklists[0], self.steppage)


class DashboardViewTestCase(TestCase):

    def setUp(self):
        """Set Up User
        Set up user with permissions to access admin."""

        self.user = factories.UserFactory()
        self.user.is_staff = True
        p = Permission.objects.get(codename='access_admin')
        self.user.user_permissions.add(p)
        self.user.save()

    def test_view_redirects_to_wagtail(self):
        """Test Not Login Redirects
        Not logged in user redirects to login from dashboard.
        """
        res = self.client.get(reverse('wagalytics_dashboard'))
        new_url = "%s?next=%s" % (
            reverse('wagtailadmin_login'), reverse('wagalytics_dashboard'))

        self.assertRedirects(res, new_url)

    def test_view_returns_200(self):
        """Test Logged in User Can Access
        Logged in user goes to dashboard.
        """
        self.client.force_login(self.user)
        res = self.client.get(reverse('wagalytics_dashboard'))
        self.assertEquals(res.status_code, 200)
