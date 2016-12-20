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
from . import views as project_views



urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),

    url(r'^cms/', include(wagtailadmin_urls)),
    url(r'^documents/', include(wagtaildocs_urls)),
    url(r'^search', include('wealthmap.frontend_urls', namespace='wealthmap')),
    url(r'^accounts/', include('registration.backends.simple.urls')),
    url(r'^accounts/', include('biz_content.urls')),
    url(r'^register/complete/$', project_views.register_complete, name='register-complete'),
    url(r'^register/', CreateView.as_view(
            template_name='registration/registration_form.html',
            form_class=forms.CustomUserCreationForm,
            success_url='/register/complete/',
    		), name="register"),

    url(r'', include(urls)),

    url(r'', include(wagtail_urls))

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
