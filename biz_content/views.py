import requests
from django.views.generic import TemplateView
from django.shortcuts import render
from django.conf import settings
from django.contrib import messages
from . import forms, models
from .model_forms import ProjectNotebookForm
from urllib.parse import urljoin
import requests
from requests.exceptions import RequestException
from django.conf import settings
import json
from urllib.parse import urljoin
import os


def dashboard(request):
    return render(request, 'biz_content/dashboard.html', {})


class PermitStatusView(TemplateView):
    template_name = "biz_content/permit_status.html"
    form_class = forms.PermitStatusForm

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        permit_data = None

        if form.is_valid():
            form_data = form.cleaned_data
            permit_id = form_data['permit_id']
            try:
                r = requests.get(urljoin(settings.SYRACUSE_IPS_URL, permit_id))
            except:
                pass
            else:
                permit_data = r.json()
            if not permit_data:
                messages.error(
                    request,
                    "Your permit could not be found. Please contact the NBD.")
        return render(request,
                      self.template_name,
                      {'form': form,
                       'permit_data': permit_data})


class IPSAPIException(Exception):
    pass


def build_business_license_url(content_type, license_id):
    relative_url = '/'.join(['business_license', content_type, license_id])
    full_url = urljoin(settings.SYRACUSE_IPS_URL, relative_url)
    return full_url


def retrieve_business_license_data(content_type, license_id):
    url = build_business_license_url(content_type, license_id)

    response = requests.get(url=url)
    try:
        response.raise_for_status()
    except RequestException as ex:
        raise IPSAPIException(
            "Error from IPS API: {}".format(ex.message, sys.exc_info()[2]))
    return response.json()


class BizLicenseStatusView(TemplateView):
    template_name = "biz_content/biz_license_status.html"
    form_class = forms.BizLicenseStatusForm

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        biz_license_data = None

        if form.is_valid():
            form_data = form.cleaned_data
            cu_id = form_data['cu_id']
            application_data = retrieve_business_license_data(
                "application_data", cu_id)
            inspection_data = retrieve_business_license_data(
                "inspection_data", cu_id)
            payment_data = retrieve_business_license_data(
                "payment_data", cu_id)

            if not application_data:
                messages.error(
                    request,
                    "Your permit could not be found. Please contact the NBD.")

            else:
                biz_license_data = {"application_data": application_data,
                                    "inspection_data": inspection_data,
                                    "payment_data": payment_data}
        return render(request,
                      self.template_name,
                      {'form': form,
                       'biz_license_data': biz_license_data})
