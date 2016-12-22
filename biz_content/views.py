from biz_content.models import Project, ChecklistItem
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.admin.views.decorators import staff_member_required
from registration.backends.simple.views import RegistrationView
from django.core.urlresolvers import reverse
from . import forms
from .models import StepPage
import pdb


@login_required
def profile(request):
    steppages = StepPage.objects.all()
    if request.user.username:
        checklists = []
        empty_checklists = []
        projects = request.user.projects.all()

        project = request.user.projects.all()[0]
        for sp in steppages:
            empty_checklists.append(forms.ChecklistForm(steppage=sp, project=project))
        return render(request, 'biz_content/profile.html',
                        { 'empty_checklists':empty_checklists,
                        'projects':projects})
    else:
        return HttpResponseRedirect('/')

def dashboard(request):
    return render(request, 'biz_content/dashboard.html', {})


class UserRegistrationView(RegistrationView):
    form_class = forms.CustomUserCreationForm

    def get_success_url(self, user):
        return reverse('profile')
