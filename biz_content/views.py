from biz_content.models import Project, ChecklistItem
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.admin.views.decorators import staff_member_required
from registration.backends.simple.views import RegistrationView
from django.core.urlresolvers import reverse
from django.views.generic.edit import CreateView, UpdateView

from . import forms
from .models import StepPage

from .model_forms import ProjectNotebookForm


@login_required
def profile(request):
    steppages = StepPage.objects.all()
    projects = request.user.projects.all()
    form = None

    empty_checklists = []
    project = request.user.projects.all()[0]
    for sp in steppages:
        if sp.checklist_items.all():
            empty_checklists.append(
                forms.ChecklistForm(steppage=sp, project=project))

    for p in projects:
        p.business_information_form = ProjectNotebookForm()

        if request.GET:
            project = Project.objects.get()
            initial = {'owner': request.user}
            form = ProjectNotebookForm(initial=initial)

        if request.POST:
            form = ProjectNotebookForm(request.POST)
            if form.is_valid():
                raise
                form.save(commit=False)

    return render(
                request,
                'biz_content/profile.html', {
                    'empty_checklists': empty_checklists,
                    'projects': projects,
                    'form', form
                })


class CreateProject():
    def post(request):
        user = request.user
        number_of_projects = len(user.projects)
        name = 'Default' + str(number_of_projects)
        project = Project(name=name, owner_id=user.id)
        project.save()


def dashboard(request):
    return render(request, 'biz_content/dashboard.html', {})


class UserRegistrationView(RegistrationView):
    form_class = forms.CustomUserCreationForm

    def get_success_url(self, user):
        return reverse('profile')
