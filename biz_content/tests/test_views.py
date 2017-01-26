import responses
import json
from . import factories
from biz_content import models, forms, views
from django.test import TestCase, TransactionTestCase
from django.core.urlresolvers import reverse
from django.contrib.auth.models import Permission
from django.utils import html
from django.conf import settings
import os
from urllib.parse import urljoin


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


class BusinessLicenseViewTestCase(TestCase):

    def setUp(self):
        self.location = os.path.realpath(
            os.path.join(os.getcwd(), os.path.dirname(__file__)))
        self.application_data = open(
            os.path.join(self.location, 'application_data.json'), 'r').read()
        self.inspection_data = open(
            os.path.join(self.location, 'inspection_data.json'), 'r').read()
        self.payment_data = open(
            os.path.join(self.location, 'payment_data.json'), 'r').read()
        self.mock_urls = {"application_data": self.application_data,
                     "inspection_data": self.inspection_data,
                     "payment_data": self.payment_data}
        self.empty_mock_urls = {"application_data": '[]',
                     "inspection_data": '[]',
                     "payment_data": '[]'}

    def test_build_business_license_url(self):
        content_type = 'application_data'
        license_id = 'CU12354'
        url = views.build_business_license_url(content_type, license_id)
        business_license_url = '%sbusiness_license/%s/%s' % (
            settings.SYRACUSE_IPS_URL,
            content_type,
            license_id
        )
        self.assertEquals(url, business_license_url)

    # def test_format_business_license_inspection_data(self):
    #     location = os.path.realpath(
    #         os.path.join(os.getcwd(), os.path.dirname(__file__)))
    #     inspection_data = open(
    #         os.path.join(location, 'inspection_data.json'), 'r').read()


    @responses.activate
    def test_200_with_business_licenses(self):
        license_id = 'CU2014-0050'

        for url, data in self.mock_urls.items():
            full_url = views.build_business_license_url(url, license_id)
            responses.add(
                responses.GET, full_url,
                body=data, status=200, content_type='application/json')

        res = self.client.post(
            reverse('biz_license_status'), {
                'cu_id': license_id})
        self.assertEquals(res.status_code, 200)
        context = res.context

        self.assertEquals(
            context['biz_license_data']['application_data'],
            json.loads(str(self.application_data)))
        self.assertEquals(
            context['biz_license_data']['inspection_data'],
            json.loads(str(self.inspection_data)))
        self.assertEquals(
            context['biz_license_data']['payment_data'],
            json.loads(str(self.payment_data)))

    @responses.activate
    def test_no_business_licenses(self):
        license_id = 'CU2014-005089403'

        for url, data in self.empty_mock_urls.items():
            full_url = views.build_business_license_url(url, license_id)
            responses.add(
                responses.GET, full_url,
                body=data, status=200, content_type='application/json')

        data = {'cu_id': license_id}
        res = self.client.post(reverse('biz_license_status'), data)
        self.assertEquals(res.status_code, 200)

        context = res.context
        self.assertTrue('messages' in context)

        messages = list(context['messages'])
        err = 'Your permit could not be found. Please contact the NBD.'
        self.assertEquals(
            str(messages[0]), err)
