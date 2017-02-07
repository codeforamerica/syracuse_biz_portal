from django.conf import settings
from django.conf.urls.static import static

from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.views.generic.edit import CreateView
from django.http import HttpResponse

from biz_content import urls
from wagtail.wagtailadmin import urls as wagtailadmin_urls
from wagtail.wagtailcore import urls as wagtail_urls
from wagtail.wagtaildocs import urls as wagtaildocs_urls
from wagtail.contrib.wagtailsitemaps.views import sitemap

from biz_content import forms
from biz_content import views

robots_txt = """User-agent: *
Disallow: /cms
Disallow: /admin
Disallow: %s
""" % (settings.STATIC_URL,)

dcv = """6268AF5D5CC5EFFE9689C8FA5797F1D918C34B0A
comodoca.com
"""

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),

    url(r'^cms/', include(wagtailadmin_urls)),
    url(r'^documents/', include(wagtaildocs_urls)),
    url(r'^search', include('wealthmap.frontend_urls', namespace='wealthmap')),
    url(r'^robots\.txt$', lambda r: HttpResponse(
        robots_txt, content_type='text/plain')),
    url(r'^BDCA74ED8C6126C0EFA304E5136B611B\.txt$', lambda r: HttpResponse(
        dcv, content_type='text/plain')),
    url(r'^sitemap\.xml$', sitemap),
    url(r'', include(urls)),
    url(r'', include(wagtail_urls))

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
