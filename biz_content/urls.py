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

    url('^register/', CreateView.as_view(
            template_name='registration/register.html',
            form_class=forms.CustomUserCreationForm,
            success_url='/login/',
    ), name="register"),

    url(r'^login/$', auth_views.login, name="login"),
    url(r'^logout/$', auth_views.logout, name='logout'),
    url(r'^user/password/reset/$',
        auth_views.password_reset,
        {'post_reset_redirect': '/user/password/reset/done/'},
        name="password_reset"),
    url(r'^user/password/reset/done/$',
        auth_views.password_reset_done),
    url(r'^password_reset_confirm/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        auth_views.password_reset_confirm,
        {'post_reset_redirect': '/user/password/done/'},
        name='password_reset_confirm'),
    url(r'^user/password/done/$',
        auth_views.password_reset_complete),
]
