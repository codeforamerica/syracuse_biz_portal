import local_settings
from django.conf import settings
from django.conf.urls.static import static

from django.conf.urls import include, url
from django.contrib import admin

from biz_content import urls
from search import views as search_views
from wagtail.wagtailadmin import urls as wagtailadmin_urls
from wagtail.wagtailcore import urls as wagtail_urls
from wagtail.wagtaildocs import urls as wagtaildocs_urls

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/', include('registration.backends.simple.urls')),
    url(r'^cms/', include(wagtailadmin_urls)),
    url(r'^documents/', include(wagtaildocs_urls)),
    url(r'^search/$', search_views.search, name='search'),
    url(r'', include(urls)),
    url(r'', include(wagtail_urls)),
]

# Serve up local images if running in development
if local_settings.DEBUG is True:
    print("DEBUG")
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
