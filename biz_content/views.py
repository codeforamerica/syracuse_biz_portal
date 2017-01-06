from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.admin.views.decorators import staff_member_required
from registration.backends.simple.views import RegistrationView
from django.core.urlresolvers import reverse
from django.views.generic.base import TemplateView
from . import forms
import requests
import pdb

SYRACUSE_PERMIT_URL = 'http://24.97.110.146:8081/api/permits/'


@login_required
def profile(request):
    return render(request, 'biz_content/profile.html', {})


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
                r = requests.get(SYRACUSE_PERMIT_URL + permit_id)
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
