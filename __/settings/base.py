"""
Django settings for macdown project.

For more information on this file, see
https://docs.djangoproject.com/en/dev/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/dev/ref/settings/
"""

import os
from django.core.exceptions import ImproperlyConfigured

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))


def get_env_var(key):
    try:
        return os.environ[key]
    except KeyError:
        raise ImproperlyConfigured(
            'Environment variable {key} required.'.format(key=key)
        )


DEBUG = False
TEMPLATE_DEBUG = False
INTERNAL_IPS = ('127.0.0.1',)
ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'base',
    'downloads',
    'history',
    'pages',
    'absolute',
    'ghostdown',
    'grappelli',
    'sparkle',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'base.middleware.SecureRequiredMiddleware',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.request',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.core.context_processors.tz',
    'django.contrib.messages.context_processors.messages',
    'base.context_processors.latest_version',
)

ROOT_URLCONF = '__.urls'

WSGI_APPLICATION = '__.wsgi.application'


# Database
# https://docs.djangoproject.com/en/dev/ref/settings/#databases

DATABASES = {}

# Internationalization
# https://docs.djangoproject.com/en/dev/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Taipei'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/dev/howto/static-files/

STATIC_URL = '/static/'


# Ghostdown (for Sparkle-External)

GHOSTDOWN_MARKDOWN_RENDERER = {
    'path': 'markdown.markdown',
    'args': (),
    'kwargs': {
        'lazy_ol': False,           # Disable auto-sanitasation on OL.
        'output_format': 'html5',   # Outputs HTML5.
        'extensions': [
            'codehilite',           # Enable syntax hilighting in code blocks.
            'fenced_code',          # GitHub-flavored ``` code blocks.
            'footnotes',            # [^footnote-id] syntax.
            'smarty',               # Typographers' quotes (and others).
            'smart_strong',         # Intra-word double-underscore detection.
            'tables',               # Table syntax.
        ],
    },
}
