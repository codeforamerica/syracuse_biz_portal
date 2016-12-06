from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout


def profile(request, username):
    if username == request.user.username:
        user = User.objects.get(username=request.user.username)
        if user:
            return render(request, 'profile.html', {"username": username})
        else:
            return HttpResponseRedirect('/accounts/login')
    else:
        return HttpResponseRedirect('/accounts/login')
