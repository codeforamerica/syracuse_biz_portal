from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin
from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth import views as auth_views


from wagtail.wagtailadmin import urls as wagtailadmin_urls
from wagtail.wagtailcore import urls as wagtail_urls
from wagtail.wagtaildocs import urls as wagtaildocs_urls

from .import views


urlpatterns = [
    url(r'^profile/$', views.profile, name="profile"),
    url(r'^dashboard/$', views.dashboard, name='wagalytics_dashboard'),
    url(r'^login/$', auth_views.login, name="login"),
    url(r'^logout/$', auth_views.logout, name='logout'),
]
