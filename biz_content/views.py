from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.http import JsonResponse
from django.core.exceptions import SuspiciousOperation
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.admin.views.decorators import staff_member_required
from registration.backends.simple.views import RegistrationView
from django.core.urlresolvers import reverse
from . import forms, models


@login_required
def profile(request):
    return render(request, 'biz_content/profile.html', {})


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
    checked_items = list(checked_items.values_list('pk', flat=True))
    return redirect(request.META['HTTP_REFERER'], checked_items=checked_items)
