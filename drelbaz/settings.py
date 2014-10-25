"""
Django settings for drelbaz project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '#o)s!)gllyb)rl21lo1t=yb7kclgoqdn%o9lw8$j#!m8qztguc'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    #django
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    #third-party
    'provider',
    'provider.oauth2',
    'south',
    'tastypie',
    # 'billing',
    # 'cms',  # django CMS itself
    'mptt',  # utilities for implementing a modified pre-order traversal tree
    # 'menus',  # helper for model independent hierarchical website navigation
    'south',  # intelligent schema and data migrations
    # 'sekizai',  # for javascript and css management
    # 'djangocms_admin_style',  # for the admin skin. You **must** add 'djangocms_admin_style' in the list **before** 'django.contrib.admin'.
    'django_comments',
    'tagging',
    'zinnia',
    #local
    'accounts',
    'api',
    'misc',
)


MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.doc.XViewMiddleware',
    'django.middleware.common.CommonMiddleware',
    'cms.middleware.user.CurrentUserMiddleware',
    'cms.middleware.page.CurrentPageMiddleware',
    'cms.middleware.toolbar.ToolbarMiddleware',
    'cms.middleware.language.LanguageCookieMiddleware',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.contrib.messages.context_processors.messages',
    'django.core.context_processors.i18n',
    'django.core.context_processors.request',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'zinnia.context_processors.version',  # Optional
)


ROOT_URLCONF = 'drelbaz.urls'

WSGI_APPLICATION = 'drelbaz.wsgi.application'

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

LANGUAGES = (
    ('en-us', u'English (US)'),
    ('de', u'Deutsch'),
    ('en-gb', u'English (UK)'),
)

CMS_LANGUAGES = LANGUAGES

CMS_LANGUAGE_CONF = {
    'de': ['en-gb', 'en-us', 'fr', 'es', 'pt'],
    'en-gb': ['en-us', 'fr', 'es', 'de', 'pt'],
    'en-us': ['en-gb', 'fr', 'es', 'de', 'pt'],
}

CMS_HIDE_UNTRANSLATED = False

USE_I18N = True

USE_L10N = True

USE_TZ = False

SITE_ID = 1

### Django Merchant
MERCHANT_TEST_MODE = False
PAYPAL_TEST = MERCHANT_TEST_MODE


# Parse database configuration from $DATABASE_URL
import dj_database_url
DATABASES = {
    'default': dj_database_url.config()
}

# Honor the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Allow all host headers
ALLOWED_HOSTS = ['*']

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os, sys
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
sys.path.insert(0, os.path.join(BASE_DIR, 'drelbaz', 'apps'))

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_ROOT = '/static/'
STATIC_URL = '/static/'

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'drelbaz', 'static'),
)

MEDIA_ROOT = os.path.join(BASE_DIR, 'drelbaz', 'media')

MEDIA_URL = '/media/'

TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, 'drelbaz', 'templates'),
    os.path.join(BASE_DIR, 'drelbaz', 'templates', 'zinnia'),
    os.path.join(BASE_DIR, 'templates'),
)

CMS_TEMPLATES = (
    ('template_1.html', 'Template One'),
    ('template_2.html', 'Template Two'),
)

API_LIMIT_PER_PAGE = 0
TASTYPIE_DEFAULT_FORMATS = ['json']

APN_CERT_LOCATION = os.path.join(BASE_DIR, 'drelbaz/certs/PushNotifsCert.pem')
APN_KEY_LOCATION = os.path.join(BASE_DIR, 'drelbaz/certs/NewPushNotifsKey.pem')



try:
    from local_settings import *
except ImportError:
    pass
