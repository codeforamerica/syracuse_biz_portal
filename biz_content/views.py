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
from .model_forms import ProjectNotebookForm


@login_required
def profile(request, username):
    if username == request.user.username:
        projects = request.user.projects.all()
        for p in projects:
            p.business_information_form = ProjectNotebookForm()
        # if request.GET:
#             project = Project.objects.get()
#             initial = {'owner': request.user}
#             form = ProjectNotebookForm(initial=initial)
        if request.POST:
            form = ProjectNotebookForm(request.POST)
            if form.is_valid():
                raise
                form.save(commit=False)

        return render(
            request,
            'biz_content/profile.html',
            {'checklist': {}})
    else:
        return HttpResponseRedirect('/')


def dashboard(request):
    return render(request, 'biz_content/dashboard.html', {})


class UserRegistrationView(RegistrationView):
    form_class = forms.CustomUserCreationForm

    def get_success_url(self, user):
        return reverse('profile')
