

import os
from datetime import datetime, timedelta
from email.utils import parseaddr

import environ


env = environ.Env(DEBUG=(bool, False),)
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


def mkpath(*args):
    return os.path.abspath(os.path.join(BASE_DIR, *args))


DEBUG = env.bool('DEBUG', default=False)
SECRET_KEY = env.str('SECRET_KEY', default=('' if not DEBUG else 'xxx'))
ALLOWED_HOSTS = env('ALLOWED_HOSTS', default='').split()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
ADMINS = [parseaddr(addr) for addr in env('ADMINS', default='').split(',') if addr]

# Sending email
if env('EMAIL_HOST', default=''):
    EMAIL_HOST = env('EMAIL_HOST')
else:
    EMAIL_BACKEND = 'django.core.mail.backends.dummy.EmailBackend'

DEFAULT_FROM_EMAIL = env('DEFAULT_FROM_EMAIL', default='spam@example.com')

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'infokala',
    'infokala_tracon',
)

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

AUTHENTICATION_BACKENDS = (
    'kompassi_oauth2.backends.KompassiOAuth2AuthenticationBackend',
    'django.contrib.auth.backends.ModelBackend',
)

ROOT_URLCONF = 'infokala_tracon.urls'

WSGI_APPLICATION = 'infokala_tracon.wsgi.application'

DATABASES = {
    'default': env.db(default='sqlite:///infokala.sqlite3'),
}

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

LANGUAGE_CODE = 'fi-fi'

TIME_ZONE = 'Europe/Helsinki'

USE_I18N = True
USE_L10N = False
USE_TZ = True

STATIC_URL = '/static/'
STATIC_ROOT = mkpath('static')
APPEND_SLASH = False

LOGIN_URL = '/oauth2/login'
LOGOUT_URL = '/logout'
LOGOUT_REDIRECT_URL = 'https://kompassi.eu/logout'

from .event import get_event_or_404 as INFOKALA_GET_EVENT_OR_404

INFOKALA_ACCESS_GROUP_TEMPLATES = [
    '{infokala_installation_slug}-{event_slug}-users',
    '{kompassi_installation_slug}-{event_slug}-labour-conitea',
    '{kompassi_installation_slug}-{event_slug}-labour-info',
    '{kompassi_installation_slug}-{event_slug}-labour-jarjestyksenvalvoja',
    '{kompassi_installation_slug}-{event_slug}-labour-jv',
]
INFOKALA_DEFAULT_EVENT = env('INFOKALA_DEFAULT_EVENT', default='tracon2017')
INFOKALA_INSTALLATION_SLUG = env('INFOKALA_INSTALLATION_SLUG', default='infokala')

KOMPASSI_INSTALLATION_SLUG = env('KOMPASSI_INSTALLATION_SLUG', default='turska')
KOMPASSI_HOST = env('KOMPASSI_HOST', default='https://kompassi.eu')
KOMPASSI_OAUTH2_AUTHORIZATION_URL = '{KOMPASSI_HOST}/oauth2/authorize'.format(**locals())
KOMPASSI_OAUTH2_TOKEN_URL = '{KOMPASSI_HOST}/oauth2/token'.format(**locals())
KOMPASSI_OAUTH2_CLIENT_ID = env('KOMPASSI_OAUTH2_CLIENT_ID', default='kompassi_insecure_test_client_id')
KOMPASSI_OAUTH2_CLIENT_SECRET = env('KOMPASSI_OAUTH2_CLIENT_SECRET', default='kompassi_insecure_test_client_secret')
KOMPASSI_OAUTH2_SCOPE = ['read']
KOMPASSI_API_V2_USER_INFO_URL = '{KOMPASSI_HOST}/api/v2/people/me'.format(**locals())
KOMPASSI_API_V2_EVENT_INFO_URL_TEMPLATE = '{kompassi_host}/api/v2/events/{event_slug}'
KOMPASSI_ADMIN_GROUP = env('KOMPASSI_ADMIN_GROUP', default='admins')
