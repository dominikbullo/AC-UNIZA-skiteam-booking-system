"""
Django settings for app project.

Generated by 'django-admin startproject' using Django 2.2.6.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import sys

from django.urls import include

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
SETTINGS_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE_DIR = os.path.dirname(SETTINGS_DIR)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '200)k4*f_240=jwb2qsn#q(njow#e6%mm&kdrop9*6%v%zd7u+'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
ALLOWED_HOSTS = ['*']

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'whitenoise.runserver_nostatic',  # < Per Whitenoise, to disable built in
    'django.contrib.staticfiles',
    'django.contrib.sites',

    'users',
    'family',
    'events',

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

    # 'widget_tweaks',
]

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
# RELEASE: Dont forget to add your client's address to the CORS whitelist.
#   This will make sure the server accepts request from the specified source only

CORS_ORIGIN_WHITELIST = [
    'http://localhost:3000',
    'http://localhost:8000',
    'http://localhost:8080',
]

# # allow all requests containing any of the default headers(as in django docs) or content-type header
# CORS_ALLOW_HEADERS = default_headers + (
#     'contenttype',
# )

ROOT_URLCONF = 'app.urls'

TEMPLATES = [
    {
        'BACKEND' : 'django.template.backends.django.DjangoTemplates',
        'DIRS'    : ['../frontend/dist'],
        'APP_DIRS': True,
        'OPTIONS' : {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'app.wsgi.application'

# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME'  : os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_URL = '/static/'
# Place static in the same location as webpack build files
STATIC_ROOT = os.path.join(os.path.dirname(BASE_DIR), 'frontend', 'dist')
STATICFILES_DIRS = [
    os.path.join(STATIC_ROOT, 'static'),
]
# Custom User Model
AUTH_USER_MODEL = "users.User"

SITE_ID = 1

AUTHENTICATION_BACKENDS = (
    # Needed to login by username in Django admin, regardless of `allauth`
    # 'users.auth.CustomEmailAuthBackend.EmailAuthBackend'
    "django.contrib.auth.backends.ModelBackend",

    # `allauth` specific authentication methods, such as login by e-mail
    "allauth.account.auth_backends.AuthenticationBackend",
)
# EMAIL_BACKEND so allauth can proceed to send confirmation emails
# ONLY for development/testing use console
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

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
DATE_INPUT_FORMATS = [
    ("%d.%m.%Y"),
]

# http://whitenoise.evans.io/en/stable/#quickstart-for-django-apps
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Django-REST-Framework
# https://medium.com/@apogiatzis/create-a-restful-api-with-users-and-jwt-authentication-using-django-1-11-drf-part-2-eb6fdcf71f45
REST_FRAMEWORK = {
    "DATE_INPUT_FORMATS"            : DATE_INPUT_FORMATS,
    'DEFAULT_PERMISSION_CLASSES'    : ('rest_framework.permissions.IsAuthenticated',),
    'DEFAULT_AUTHENTICATION_CLASSES': ('rest_framework.authentication.TokenAuthentication',
                                       # RELEASE Delete SessionAuthentication
                                       'rest_framework.authentication.SessionAuthentication',
                                       ),
    'DEFAULT_PAGINATION_CLASS'      : 'rest_framework.pagination.PageNumberPagination',

    # FIXME on front
    'PAGE_SIZE'                     : 100
}

try:
    from .local_settings import *
except ImportError:
    pass
