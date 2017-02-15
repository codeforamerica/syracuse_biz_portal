import requests
import os
import datetime
import sys
import json

from django.views.generic import TemplateView
from django.shortcuts import render
from django.conf import settings
from django.contrib import messages
from . import forms, models
from requests.exceptions import ConnectionError, HTTPError, Timeout
from urllib.parse import urljoin


def dashboard(request):
    return render(request, 'biz_content/dashboard.html', {})


class IPSAPIException(Exception):
    pass


def build_business_license_url(content_type, license_id):
    relative_url = '/'.join(['business_license', content_type, license_id])
    full_url = urljoin(settings.SYRACUSE_IPS_URL, relative_url)
    return full_url


def build_permit_url(permit_id):
    relative_url = '/'.join(['permits', permit_id])
    full_url = urljoin(settings.SYRACUSE_IPS_URL, relative_url)
    return full_url


def create_datetime_object(date):
    string_date = date[0:][:10]
    d = datetime.datetime.strptime(string_date, "%Y-%m-%d")
    return d


def get_most_recent_license_status(application_data):
    application_dates = [
        create_datetime_object(d['action_date']) for d in application_data]
    now = datetime.datetime.now()
    youngest = max(dt for dt in application_dates if dt < now)
    most_recent_status = [dt for dt in application_data
                          if create_datetime_object(
                              dt['action_date']) == youngest]
    return most_recent_status[0]


def format_license_inspection(inspection_data):
    inspection_dates = [
        create_datetime_object(d['inspect_date']) for d in inspection_data]
    formatted_inspection_data = {}
    years = set([d.year for d in inspection_dates])
    for y in years:
        formatted_inspection_data[y] = []
    for inspection in inspection_data:
        inspect_date = create_datetime_object(inspection['inspect_date'])
        formatted_inspection_data[inspect_date.year].append(inspection)
    return formatted_inspection_data


def proxy_requests(url):
    if settings.IPS_PROXIES:
        return requests.get(url=url, proxies=settings.IPS_PROXIES)
    else:
        return requests.get(url=url)


def retrieve_business_license_data(content_type, license_id):
    url = build_business_license_url(content_type, license_id)

    try:
        response = proxy_requests(url)
    except (Timeout, ConnectionError) as ex:
        raise IPSAPIException("Error from IPS API")

    if response.status_code == 500:
        raise IPSAPIException("500 error")

    return response.json()


def retrieve_permit_data(permit_id):
    url = build_permit_url(permit_id)

    try:
        response = proxy_requests(url)
    except (Timeout, ConnectionError) as ex:
        raise IPSAPIException("Error from IPS API")

    if response.status_code == 500:
        raise IPSAPIException("500 error")

    return response.json()


class ChecklistView(TemplateView):
    template_name = "biz_content/checklist.html"

    def get(self, request, *args, **kwargs):
        step_pages = models.StepPage.objects.all()
        return render(request, self.template_name, {'step_pages': step_pages})


IPS_ERROR_MESSAGE = "Data from the City of Syracuse cannot be accessed."
LICENSE_NOT_FOUND_ERROR_MESSAGE = ("Your permit or business license "
                                   "could not be found. "
                                   "Please contact the NBD.")


class BizLicenseStatusView(TemplateView):
    template_name = "biz_content/biz_license_status.html"
    form_class = forms.BizLicenseStatusForm

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        biz_license_data = None
        status = 200

        if form.is_valid():
            form_data = form.cleaned_data
            cu_id = form_data['cu_id']
            try:
                application_data = retrieve_business_license_data(
                    "application_data", cu_id)

                application_data.sort(
                    key=lambda application: application['action_date'],
                    reverse=True)
                inspection_data = retrieve_business_license_data(
                    "inspection_data", cu_id)
                payment_data = retrieve_business_license_data(
                    "payment_data", cu_id)
            except IPSAPIException:
                messages.error(request, IPS_ERROR_MESSAGE)
                status = 503
            else:
                if len(application_data) == 0:
                    messages.error(
                        request, LICENSE_NOT_FOUND_ERROR_MESSAGE
                    )
                else:
                    license = models.BizLicenseSearch(license_id=cu_id).save()
                    biz_license_data = {
                        "application_data": application_data,
                        "inspection_data": format_license_inspection(
                            inspection_data),
                        "payment_data": payment_data,
                        "current_status": get_most_recent_license_status(
                            application_data)
                    }

        return render(request,
                      self.template_name,
                      {'form': form,
                       'biz_license_data': biz_license_data}, status=status)


class PermitStatusView(TemplateView):
    template_name = "biz_content/permit_status.html"
    form_class = forms.PermitStatusForm

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        permit_data = None
        status = 200

        if form.is_valid():
            form_data = form.cleaned_data
            permit_id = form_data['permit_id']
            try:
                permit_data = retrieve_permit_data(permit_id)
            except IPSAPIException:
                messages.error(request, IPS_ERROR_MESSAGE)
                status = 503
            else:
                if len(permit_data) == 0:
                    messages.error(
                        request, LICENSE_NOT_FOUND_ERROR_MESSAGE
                    )
                else:
                    permit_data = permit_data

        return render(request,
                      self.template_name,
                      {'form': form,
                       'permit_data': permit_data}, status=status)
