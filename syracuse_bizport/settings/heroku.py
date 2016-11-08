import os
import dj_database_url
from .base import *


SECRET_KEY = os.environ['DJANGO_SECRET_KEY']

DATABASES['default'] = dj_database_url.config()

# Honor the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Allow all host headers
ALLOWED_HOSTS = ['*']

STATIC_ROOT = os.path.join(BASE_DIR, '../staticfiles')

STATICFILES_STORAGE = 'whitenoise.django.GzipManifestStaticFilesStorage'
