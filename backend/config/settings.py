"""
Django settings for SportAgenda project.

For more information on this file, see
https://docs.djangoproject.com/en/dev/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/dev/ref/settings/
"""
import environ
from datetime import timedelta

ROOT_DIR= environ.Path(__file__) - 2
APP_DIR = environ.Path(__file__) - 3
# SETTINGS_DIR = environ.Path(__file__)
# BASE_DIR = environ.Path(__file__) - 1
# FRONTEND_DIR = str(APP_DIR('frontend'))

# Load operating system environment variables and then prepare to use them
env = environ.Env()

# APP CONFIGURATION
# ------------------------------------------------------------------------------
DJANGO_APPS = [
    # https://github.com/deschler/django-modeltranslation/issues/408
    'modeltranslation',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'whitenoise.runserver_nostatic',
    'django.contrib.staticfiles',
    'django.contrib.sites',
]

THIRD_PARTY_APPS = [
    'django_extensions',

    'rest_framework',
    'rest_framework.authtoken',
    'rest_auth',

    # https://django-rest-auth.readthedocs.io/en/latest/api_endpoints.html
    'allauth',
    'allauth.account',
    'rest_auth.registration',

    # https://github.com/adamchainz/django-cors-headers#cors_allow_headers
    'corsheaders',

    # https://django-rest-auth.readthedocs.io/en/latest/installation.html
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    'allauth.socialaccount.providers.facebook',

    'polymorphic',

    'pwa',

    'simple_mail',
    'ckeditor',

    'django_excel_fixture',
    'django_filters',
]

LOCAL_APPS = [
    'apps.users',
    'apps.family',
    'apps.events',
]
# See: https://docs.djangoproject.com/en/dev/ref/settings/#installed-apps
INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

# MIDDLEWARE CONFIGURATION
# ------------------------------------------------------------------------------
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    # 'app.middleware.LoginRequiredMiddleware',
    'corsheaders.middleware.CorsMiddleware',
]

# DEBUG
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#debug
DEBUG = env.bool('DEBUG')
SECRET_KEY = env.str('SECRET_KEY')

# DOMAINS
ALLOWED_HOSTS = env.list('ALLOWED_HOSTS', default=['*'])
DOMAIN = env.str('DOMAIN')

# EMAIL CONFIGURATION
# ------------------------------------------------------------------------------
EMAIL_PORT = env.int('EMAIL_PORT', default='1025')
EMAIL_HOST = env.str('EMAIL_HOST', default='mailhog')

# MANAGER CONFIGURATION
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#admins
ADMINS = [
    ('Dominik Bullo', 'admin@acuniza.skiteam.sk'),
]

# See: https://docs.djangoproject.com/en/dev/ref/settings/#managers
MANAGERS = ADMINS

# DATABASE CONFIGURATION
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME'  : str(ROOT_DIR('db.sqlite3')),
    }
}

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql_psycopg2',
#         'NAME': env.str('POSTGRES_DB'),
#         'USER': env.str('POSTGRES_USER'),
#         'PASSWORD': env.str('POSTGRES_PASSWORD'),
#         'HOST': 'postgres',
#         'PORT': 5432,
#     },
# }

# GENERAL CONFIGURATION
# ------------------------------------------------------------------------------
# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'Europe/Bratislava'

# See: https://docs.djangoproject.com/en/dev/ref/settings/#language-code
LANGUAGE_CODE = 'en-us'

# See: https://docs.djangoproject.com/en/dev/ref/settings/#use-i18n
USE_I18N = True

# See: https://docs.djangoproject.com/en/dev/ref/settings/#use-l10n
USE_L10N = True

# See: https://docs.djangoproject.com/en/dev/ref/settings/#use-tz
USE_TZ = True

# STATIC FILE CONFIGURATION
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#static-root
STATIC_ROOT = str(ROOT_DIR('staticfiles'))

# See: https://docs.djangoproject.com/en/dev/ref/settings/#static-url
STATIC_URL = '/staticfiles/'

# See: https://docs.djangoproject.com/en/dev/ref/contrib/staticfiles/#std:setting-STATICFILES_DIRS
STATICFILES_DIRS = [
    str(ROOT_DIR('static')),
]

# See: https://docs.djangoproject.com/en/dev/ref/contrib/staticfiles/#staticfiles-finders
STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
]

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# MEDIA CONFIGURATION
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#media-root
MEDIA_ROOT = str(ROOT_DIR('media'))

# See: https://docs.djangoproject.com/en/dev/ref/settings/#media-url
MEDIA_URL = '/media/'

# URL Configuration
# ------------------------------------------------------------------------------
ROOT_URLCONF = 'config.urls'

# See: https://docs.djangoproject.com/en/dev/ref/settings/#wsgi-application
WSGI_APPLICATION = 'config.wsgi.application'

# TEMPLATE CONFIGURATION
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#templates
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': STATICFILES_DIRS,
        'OPTIONS': {
            'debug': DEBUG,
            'loaders': [
                'django.template.loaders.filesystem.Loader',
                'django.template.loaders.app_directories.Loader',
            ],
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]


# PASSWORD STORAGE SETTINGS
# ------------------------------------------------------------------------------
# See https://docs.djangoproject.com/en/dev/ref/settings/#password-hashers
PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.PBKDF2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',
    'django.contrib.auth.hashers.Argon2PasswordHasher',
    'django.contrib.auth.hashers.BCryptSHA256PasswordHasher',
    'django.contrib.auth.hashers.BCryptPasswordHasher',
]

# PASSWORD VALIDATION
# https://docs.djangoproject.com/en/dev/ref/settings/#auth-password-validators
# ------------------------------------------------------------------------------
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# AUTHENTICATION CONFIGURATION
# ------------------------------------------------------------------------------
AUTHENTICATION_BACKENDS = (
    # Needed to login by username in Django admin, regardless of `allauth`
    # 'users.auth.CustomEmailAuthBackend.EmailAuthBackend'
    "django.contrib.auth.backends.ModelBackend",

    # `allauth` specific authentication methods, such as login by e-mail
    "allauth.account.auth_backends.AuthenticationBackend",
)
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Custom user app defaults
# Select the correct user model
AUTH_USER_MODEL = 'users.User'

SITE_ID = 1


# DJANGO REST FRAMEWORK
# ------------------------------------------------------------------------------
# In signup for parent
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_UNIQUE_EMAIL = True
OLD_PASSWORD_FIELD_ENABLED = True

ACCOUNT_AUTHENTICATION_METHOD = 'username_email'

CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_CREDENTIALS = True

REST_AUTH_REGISTER_SERIALIZERS = {
    'REGISTER_SERIALIZER': 'users.api.serializers.CustomRegisterSerializer',
}
REST_AUTH_SERIALIZERS = {
    # 'USER_DETAILS_SERIALIZER': 'users.api.serializers.CustomUserDetailSerializer',
    'TOKEN_SERIALIZER': 'users.api.serializers.TokenSerializer',
}
CALENDAR_DATETIME_FORMAT = '%Y-%m-%d %H:%M'
DATETIME_FORMAT = '%d.%m.%Y %H:%M'
DATE_FORMAT = "%d.%m.%Y"

# Django-REST-Framework
# https://medium.com/@apogiatzis/create-a-restful-api-with-users-and-jwt-authentication-using-django-1-11-drf-part-2-eb6fdcf71f45
REST_FRAMEWORK = {
    "DATETIME_INPUT_FORMATS"        : [(DATETIME_FORMAT), ('iso-8601')],
    "DATE_INPUT_FORMATS"            : [('iso-8601'), ],
    'DEFAULT_FILTER_BACKENDS'       : ['django_filters.rest_framework.DjangoFilterBackend'],
    'DEFAULT_PERMISSION_CLASSES'    : ('rest_framework.permissions.IsAuthenticated',),
    'DEFAULT_AUTHENTICATION_CLASSES': ('rest_framework.authentication.TokenAuthentication',
                                       # RELEASE Delete SessionAuthentication
                                       'rest_framework.authentication.SessionAuthentication',
                                       ),
    'DEFAULT_PAGINATION_CLASS'      : 'rest_framework.pagination.PageNumberPagination',

    # FIXME on front
    'PAGE_SIZE'                     : 100
}


# raven sentry client
# See https://docs.sentry.io/clients/python/integrations/django/
INSTALLED_APPS += ['raven.contrib.django.raven_compat']
RAVEN_MIDDLEWARE = ['raven.contrib.django.raven_compat.middleware.SentryResponseErrorIdMiddleware']
MIDDLEWARE = RAVEN_MIDDLEWARE + MIDDLEWARE

# Sentry Configuration
SENTRY_DSN = env.str('SENTRY_DSN')
SENTRY_CLIENT = 'raven.contrib.django.raven_compat.DjangoClient'
LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'root': {
        'level': 'WARNING',
        'handlers': ['sentry'],
    },
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s '
                      '%(process)d %(thread)d %(message)s'
        },
    },
    'handlers': {
        'sentry': {
            'level': 'ERROR',
            'class': 'raven.contrib.django.raven_compat.handlers.SentryHandler',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        }
    },
    'loggers': {
        'django.db.backends': {
            'level': 'ERROR',
            'handlers': ['console'],
            'propagate': False,
        },
        'raven': {
            'level': 'DEBUG',
            'handlers': ['console'],
            'propagate': False,
        },
        'sentry.errors': {
            'level': 'DEBUG',
            'handlers': ['console'],
            'propagate': False,
        },
        'django.security.DisallowedHost': {
            'level': 'ERROR',
            'handlers': ['console', 'sentry'],
            'propagate': False,
        },
    },
}

RAVEN_CONFIG = {
    'DSN': SENTRY_DSN
}

# enable django-ckeditor integration
SIMPLE_MAIL_USE_CKEDITOR = True
