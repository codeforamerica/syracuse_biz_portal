import os
import dj_database_url
from .base import *


SECRET_KEY = os.environ['DJANGO_SECRET_KEY']

AWS_ACCESS_ID = os.environ['BUCKETEER_AWS_ACCESS_KEY_ID']
AWS_SECRET_ACCESS_KEY = os.environ['BUCKETEER_AWS_SECRET_ACCESS_KEY']

AWS_STORAGE_BUCKET_NAME = os.environ['BUCKETEER_BUCKET_NAME']

DATABASES['default'] = dj_database_url.config()

# Honor the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Allow all host headers
ALLOWED_HOSTS = ['*']

STATIC_ROOT = os.path.join(PROJECT_ROOT, '../staticfiles')

STATICFILES_STORAGE = 'whitenoise.django.GzipManifestStaticFilesStorage'
