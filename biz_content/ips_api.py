import requests
from django.contrib.auth.models import User
from requests.exceptions import RequestException
import sys
from django.conf import settings
import json
from django.core.mail import send_mail


class IPSAPIException(Exception):
    pass


class IPSAPIClient():

    def __init__(self, license_id):
        self.url = settings.SYRACUSE_IPS_URL
        self.application_data = self.retrieve_business_license_data(
            'application_data', license_id)
        self.payment_data = self.retrieve_business_license_data(
            'payment_data', license_id)
        self.inspection_data = self.retrieve_business_license_data(
            'inspection_data', license_id)

    def retrieve_business_license_data(self, content_type, license_id):
        url = self.url + "business_license/" + \
            content_type + "/" + str(license_id)
        response = requests.get(url=url)
        try:
            response.raise_for_status()
        except RequestException as ex:
            raise IPSAPIException(
                "Error from IPS API: {}".format(ex.message, sys.exc_info()[2]))
        return response.json()

    @classmethod
    def from_settings(cls, settings):
        return cls(settings.SYRACUSE_IPS_URL)
