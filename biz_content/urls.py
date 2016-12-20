from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin
from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.views.generic.edit import CreateView
from django.contrib.auth.forms import UserCreationForm

from wagtail.wagtailadmin import urls as wagtailadmin_urls
from wagtail.wagtailcore import urls as wagtail_urls
from wagtail.wagtaildocs import urls as wagtaildocs_urls

from . import forms
from .import views


urlpatterns = [
    url(r'^profile/$', views.profile, name="profile"),
]
