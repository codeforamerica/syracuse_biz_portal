from biz_content.models import Project, ChecklistItem
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import TemplateView

from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.core.exceptions import SuspiciousOperation
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.admin.views.decorators import staff_member_required
from registration.backends.simple.views import RegistrationView
from django.core.urlresolvers import reverse
from django.views.generic.edit import CreateView, UpdateView
from django.contrib import messages


from .models import StepPage
from .model_forms import ProjectNotebookForm
from . import forms, models

PROJECT_SUCCESS = 'Your project has saved.'
PROJECT_FAILURE = 'Your project could not be saved.'


@login_required
def profile(request):
    project_id = int(request.user.projects.all().order_by('name').first().id)

    if request.method == 'POST':
        project_id = int(request.POST['id'])
        instance = get_object_or_404(Project, id=project_id)
        form = ProjectNotebookForm(request.POST, instance=instance)
        # import pdb;pdb.set_trace()
        if form.is_valid():
            form.save()
            messages.success(request, PROJECT_SUCCESS)
        else:
            messages.error(request, PROJECT_FAILURE)

    projects = request.user.projects.all().order_by('name')
    # projects in projects
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
