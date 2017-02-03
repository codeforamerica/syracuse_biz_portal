import responses
import json
import os
import datetime
import ast

from . import factories
from biz_content import models, forms, views
from django.test import TestCase, TransactionTestCase
from django.core.urlresolvers import reverse
from django.contrib.auth.models import Permission
from django.utils import html
from django.conf import settings
from requests.exceptions import ConnectionError, HTTPError, Timeout
from urllib.parse import urljoin
from unittest.mock import patch


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

    def test_create_datetime_object(self):
        d = '2014-09-15T13:00:25'
        date = views.create_datetime_object(d)
        datetime_object = datetime.datetime.strptime('2014-09-15', "%Y-%m-%d")
        self.assertEquals(date, datetime_object)

    def test_get_most_recent_busines_license_status(self):
        app_data = json.loads(self.application_data)
        status = views.get_most_recent_license_status(app_data)
        self.assertEquals(status['action_date'], '2016-08-02T14:19:37.117')

    def test_format_license_inspection_data(self):
        json_inspection_data = json.loads(self.inspection_data)
        cleaned_data = views.format_license_inspection(
            json_inspection_data)
        self.assertEquals(list(cleaned_data.keys()), [2016, 2014])

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
            views.format_license_inspection(
                json.loads(self.inspection_data)))
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
        err = views.LICENSE_NOT_FOUND_ERROR_MESSAGE
        self.assertEquals(
            str(messages[0]), err)

    @responses.activate
    def test_retrieve_business_license_data_with_timeout(self):
        license_id = 'CU2014-0050'

        full_url = views.build_business_license_url(
            "application_data", license_id)

        def raise_timeout(request):
            raise Timeout

        responses.add_callback(
            responses.GET, full_url,
            callback=raise_timeout,
            content_type='application/json')

        with self.assertRaises(views.IPSAPIException):
            views.retrieve_business_license_data(
                "application_data", license_id)

    @responses.activate
    def test_retrieve_business_license_data_with_connection_error(self):
        license_id = 'CU2014-0050'

        full_url = views.build_business_license_url(
            "application_data", license_id)

        def raise_connection_error(request):
            raise ConnectionError

        responses.add_callback(
            responses.GET, full_url,
            callback=raise_connection_error,
            content_type='application/json')

        with self.assertRaises(views.IPSAPIException):
            views.retrieve_business_license_data(
                "application_data", license_id)

    @responses.activate
    def test_retrieve_business_license_data_with_500(self):
        license_id = 'CU2014-0050'

        full_url = views.build_business_license_url(
            "application_data", license_id)

        responses.add(
            responses.GET, full_url, body='',
            status=500,
            content_type='application/json')

        with self.assertRaises(views.IPSAPIException):
            views.retrieve_business_license_data(
                "application_data", license_id)

    @patch('biz_content.views.retrieve_business_license_data')
    def test_ips_error_creates_user_message_and_503(self, mock_retrieve):
        license_id = 'CU2014-0050'
        mock_retrieve.side_effect = views.IPSAPIException()

        res = self.client.post(
            reverse('biz_license_status'), {
                'cu_id': license_id})

        self.assertEquals(res.status_code, 503)
        context = res.context
        self.assertTrue('messages' in context)

        messages = list(context['messages'])
        err = views.IPS_ERROR_MESSAGE
        self.assertEquals(
            str(messages[0]), err)
