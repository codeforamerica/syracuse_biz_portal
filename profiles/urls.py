from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin

from search import views as search_views
from wagtail.wagtailadmin import urls as wagtailadmin_urls
from wagtail.wagtailcore import urls as wagtail_urls
from wagtail.wagtaildocs import urls as wagtaildocs_urls

from .import views

urlpatterns = [
    url(r'^profile/(\w+)/$', views.profile, name="profile"),
    url(r'', include('registration.backends.simple.urls')),
]
