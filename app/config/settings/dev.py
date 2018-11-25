from .base import *

DEV_JSON = json.load(open(os.path.join(SECRETS_DIR, 'dev.json')))
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
]

WSGI_APPLICATION = 'config.wsgi.dev.application'


# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

DATABASES = DEV_JSON['DATABASES']

AWS_STORAGE_BUCKET_NAME = DEV_JSON['AWS_STORAGE_BUCKET_NAME']

STATIC_DIR = os.path.join(BASE_DIR, 'static')

STATICFILES_DIRS = [
    STATIC_DIR,
]

# dev tools
INSTALLED_APPS.append('django_extensions')
