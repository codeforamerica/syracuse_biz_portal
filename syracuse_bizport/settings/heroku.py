import os
import dj_database_url
from .base import *

SECRET_KEY = os.environ['DJANGO_SECRET_KEY']

AWS_ACCESS_KEY_ID = os.environ['BUCKETEER_AWS_ACCESS_KEY_ID']
AWS_SECRET_ACCESS_KEY = os.environ['BUCKETEER_AWS_SECRET_ACCESS_KEY']

AWS_STORAGE_BUCKET_NAME = os.environ['BUCKETEER_BUCKET_NAME']
AWS_S3_FILE_OVERWRITE = False

DATABASES['default'] = dj_database_url.config()

# Honor the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Allow all host headers
ALLOWED_HOSTS = ['*']

STATIC_ROOT = os.path.join(PROJECT_ROOT, '../staticfiles')

STATICFILES_STORAGE = 'whitenoise.django.GzipManifestStaticFilesStorage'

MEDIA_URL = "https://%s.s3.amazonaws.com/" % (AWS_ACCESS_KEY_ID)
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto.S3BotoStorage'

EMAIL_HOST_USER = os.environ['SENDGRID_USERNAME']
EMAIL_HOST_PASSWORD = os.environ['SENDGRID_PASSWORD']
EMAIL_HOST = 'smtp.sendgrid.net'
EMAIL_PORT = 587
EMAIL_USE_TLS = True

ADMINS = ['mikela@codeforamerica.org', ]

# HTTPS EVERYWHERE
SECURE_SSL_REDIRECT = False
