from syracuse_bizport.settings.base import *

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '111111111'

# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'syracuse_biz_portal',
    }
}

# Print emails to console for easy development.
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Before setting this to `False`, make sure to set ALLOWED_HOSTS
DEBUG = True
