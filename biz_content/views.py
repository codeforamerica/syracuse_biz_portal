from biz_content.models import Project, ChecklistItem
from django.shortcuts import render
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

from .models import StepPage
from .model_forms import ProjectNotebookForm
from . import forms, models


@login_required
def profile(request):
    projects = request.user.projects.all()

    if request.method == 'GET':
        for p in projects:
            initial = {'id':p.id, 'owner_id':request.user.id}
            p.notebook_form = ProjectNotebookForm(initial)

    if request.method == 'POST':
        project_id = request.POST['id']
        instance = get_object_or_404(Project, id=project_id)
        form = ProjectNotebookForm(request.POST, instance=instance)
        if form.is_valid:
            form.save()

    return render(
            request,
            'biz_content/profile.html', {
                'projects': projects
            })

def update_project(request):
    if request.method == 'POST':
        p.notebook_form = ProjectNotebookForm(request.POST)
        p.notebook_form.save()
        data = {'success':True}
        return JsonResponse(data, status_code = 200)


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
