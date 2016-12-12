try:
    import local_settings
except ImportError:
    pass

from django.conf import settings
from django.conf.urls.static import static

from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin

from biz_content import urls
from wagtail.wagtailadmin import urls as wagtailadmin_urls
from wagtail.wagtailcore import urls as wagtail_urls
from wagtail.wagtaildocs import urls as wagtaildocs_urls

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/', include('registration.backends.simple.urls')),
    url(r'^cms/', include(wagtailadmin_urls)),
    url(r'^documents/', include(wagtaildocs_urls)),
    url(r'', include(urls)),
    url(r'', include(wagtail_urls)),
<<<<<<< HEAD
]

# Serve up local images if running locally
try:
    if local_settings.DEBUG is True:
        urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
except AttributeError:
    pass
=======
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
>>>>>>> master
