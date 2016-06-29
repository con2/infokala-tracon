import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

def mkpath(*args):
    return os.path.abspath(os.path.join(BASE_DIR, *args))

SECRET_KEY = '826)vr#_u+^taupre9!ixzb9(qxmyadij6v^jy%l+5pvd0*tv8'

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ALLOWED_HOSTS = []

if DEBUG:
    # XXX Monkey patch is_secure_transport to allow development over insecure HTTP

    from warnings import warn
    warn(UserWarning("Monkey_patching oauthlib.oauth2:is_secure_transport to allow OAuth2 over HTTP. Never do this in production!"))

    fake_is_secure_transport = lambda token_url: True

    import oauthlib.oauth2
    import requests_oauthlib.oauth2_session
    import oauthlib.oauth2.rfc6749.parameters
    import oauthlib.oauth2.rfc6749.clients.base

    for module in [
        oauthlib.oauth2,
        requests_oauthlib.oauth2_session,
        oauthlib.oauth2.rfc6749.parameters,
        oauthlib.oauth2.rfc6749.clients.base,
    ]:
        module.is_secure_transport = fake_is_secure_transport

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

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

AUTHENTICATION_BACKENDS = (
    'kompassi_oauth2.backends.KompassiOAuth2AuthenticationBackend',
    'django.contrib.auth.backends.ModelBackend',
)

ROOT_URLCONF = 'infokala_tracon.urls'

WSGI_APPLICATION = 'infokala_tracon.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

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
    '{kompassi_installation_slug}-{event_slug}-labour-conitea',
    '{kompassi_installation_slug}-{event_slug}-labour-info',
]
INFOKALA_DEFAULT_EVENT = 'finncon2016'

KOMPASSI_INSTALLATION_SLUG = 'turskadev'
KOMPASSI_HOST = 'http://kompassi.dev:8000'
KOMPASSI_OAUTH2_AUTHORIZATION_URL = '{KOMPASSI_HOST}/oauth2/authorize'.format(**locals())
KOMPASSI_OAUTH2_TOKEN_URL = '{KOMPASSI_HOST}/oauth2/token'.format(**locals())
KOMPASSI_OAUTH2_CLIENT_ID = 'kompassi_insecure_test_client_id'
KOMPASSI_OAUTH2_CLIENT_SECRET = 'kompassi_insecure_test_client_secret'
KOMPASSI_OAUTH2_SCOPE = ['read']
KOMPASSI_API_V2_USER_INFO_URL = '{KOMPASSI_HOST}/api/v2/people/me'.format(**locals())
KOMPASSI_API_V2_EVENT_INFO_URL_TEMPLATE = '{kompassi_host}/api/v2/events/{event_slug}'
KOMPASSI_ADMIN_GROUP = 'admins'
