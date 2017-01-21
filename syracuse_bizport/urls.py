from django.conf import settings
from django.conf.urls.static import static

from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.views.generic.edit import CreateView
from django.contrib.auth import views as auth_views


from biz_content import urls
from wagtail.wagtailadmin import urls as wagtailadmin_urls
from wagtail.wagtailcore import urls as wagtail_urls
from wagtail.wagtaildocs import urls as wagtaildocs_urls

from biz_content import forms
from biz_content import views


urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),

    url(r'^cms/', include(wagtailadmin_urls)),
    url(r'^documents/', include(wagtaildocs_urls)),
    url(r'^search', include('wealthmap.frontend_urls', namespace='wealthmap')),
    url(r'^accounts/register/', views.UserRegistrationView.as_view(),
        name='registration_register'),
    url(r'^accounts/', include('registration.backends.simple.urls')),
    url(r'', include(urls, namespace='biz_content')),
    url(r'', include(wagtail_urls))

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
