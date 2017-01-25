import requests
from biz_content.models import Project, ChecklistItem
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView, UpdateView
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.core.exceptions import SuspiciousOperation
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.admin.views.decorators import staff_member_required
from registration.backends.simple.views import RegistrationView
from django.core.urlresolvers import reverse
from . import forms, models
from .model_forms import ProjectNotebookForm
from urllib.parse import urljoin
import requests
from requests.exceptions import RequestException
from django.conf import settings
import json
from urllib.parse import urljoin
import os


PROJECT_SUCCESS = 'Your project has saved.'
PROJECT_FAILURE = 'Your project could not be saved.'


@login_required
def profile(request):
    project_id = int(request.user.projects.all().order_by('name').first().id)

    if request.method == 'POST':
        project_id = int(request.POST['id'])
        instance = get_object_or_404(Project, id=project_id)
        form = ProjectNotebookForm(request.POST, instance=instance)
        if form.is_valid():
            form.save()
            messages.success(request, PROJECT_SUCCESS)
        else:
            messages.error(request, PROJECT_FAILURE)

    projects = request.user.projects.all().order_by('name')
    for p in projects:
        initial = p.__dict__
        p.notebook_form = ProjectNotebookForm(initial)

    return render(
        request,
        'biz_content/profile.html', {
            'projects': projects,
            'project_id': project_id
        })


def dashboard(request):
    return render(request, 'biz_content/dashboard.html', {})


class UserRegistrationView(RegistrationView):
    form_class = forms.CustomUserCreationForm

    def get_success_url(self, user):
        return reverse('profile')


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
    full_url =urljoin(settings.SYRACUSE_IPS_URL, relative_url)
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
            # application_data = retrieve_business_license_data("application_data", cu_id)
            # inspection_data = retrieve_business_license_data("inspection_data", cu_id)
            # payment_data = retrieve_business_license_data("payment_data", cu_id)
            location = os.path.realpath(
            os.path.join(os.getcwd(), os.path.dirname(__file__)))
            application_data = open(
                                os.path.join(location, 'application_data.json'), 'r').read()
            inspection_data = open(
                                os.path.join(location, 'inspection_data.json'), 'r').read()
            payment_data = open(
                            os.path.join(location, 'payment_data.json'), 'r').read()
            if not application_data:
                messages.error(
                    request,
                    "Your permit could not be found. Please contact the NBD.")

                return redirect('biz_license_status')
            else:
                biz_license_data = {"application_data":application_data,
                            "inspection_data":inspection_data,
                            "payment_data":payment_data}
        return render(request,
                      self.template_name,
                      {'form': form,
                       'biz_license_data': biz_license_data})



@login_required
def update_checkbox(request, steppage_id, project_id):
    if not request.POST:
        raise SuspiciousOperation("Invalid request")
    steppage = get_object_or_404(models.StepPage, pk=steppage_id)
    project = request.user.projects.get(pk=project_id)
    if not project:
        raise Http404("Project does not exist")
    form = forms.ChecklistForm(steppage, request.POST, project=project)
    if form.is_valid():
        checked_items = form.save()
    else:
        raise SuspiciousOperation(str(form.POST))
    return JsonResponse({
        'checked_items': list(checked_items.values_list('pk', flat=True)),
    })
