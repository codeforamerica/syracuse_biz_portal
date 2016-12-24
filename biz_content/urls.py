from django.conf.urls import include, url
from django.conf.urls import url

from . import forms
from .import views


urlpatterns = [
    url(r'^profile/$', views.profile, name="profile"),
    url(r'^update-checkbox/(?P<steppage_id>\d+)/(?P<project_id>\d+)/$',
        views.update_checkbox, name="update_checkbox"),
]
