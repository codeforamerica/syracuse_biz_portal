from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.admin.views.decorators import staff_member_required


@login_required
def profile(request):
    return render(request, 'biz_content/profile.html', {})

def dashboard(request):
    return render(request, 'biz_content/dashboard.html', {})
