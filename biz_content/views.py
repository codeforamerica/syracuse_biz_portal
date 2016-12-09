from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout


def profile(request):
    return render(request, 'profile.html', {})


def dashboard(request):
    return render(request, 'dashboard.html', {})
