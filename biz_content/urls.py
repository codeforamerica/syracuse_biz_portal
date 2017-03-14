from django.conf.urls import include, url
from django.conf.urls import url

from . import forms
from .import views


urlpatterns = [
    url(r'^permit-status/$', views.PermitStatusView.as_view(),
        name="permit_status"),
    url(r'^biz-license-status/$',
        views.BizLicenseStatusView.as_view(),
        name="biz_license_status"),
    url(r'^checklist/$', views.ChecklistView.as_view(),
        name="checklist"),
    url(r'^api_docs/$', views.APIDocView.as_view(),
        name="api_docs"),
]
