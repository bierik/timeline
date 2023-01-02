import os
from pathlib import Path

import django_heroku

BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = "django-insecure-4t0+fq(6892+u&3s=gv48=)9487&oi6e=s&%pn00)-kj^i5g_#"
DEBUG = False
ALLOWED_HOSTS = []
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django_extensions",
    "django_filters",
    "corsheaders",
    "rest_framework",
    "django_tus",
    "django_editorjs_fields",
    'sorl.thumbnail',
    "timeline.events",
    "timeline.people",
    "timeline.image",
    "django_cleanup.apps.CleanupConfig",
]
MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]
ROOT_URLCONF = "timeline.urls"
STATIC_URL = "/static/"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
DATA_UPLOAD_MAX_MEMORY_SIZE = 5242880
TUS_UPLOAD_DIR = os.path.join(BASE_DIR, "tus_upload")
TUS_DESTINATION_DIR = os.path.join(BASE_DIR, "media", "uploads")
TUS_FILE_NAME_FORMAT = "keep"
TUS_EXISTING_FILE = "error"

REST_FRAMEWORK = {
    'PAGE_SIZE': 40,
}

AWS_STORAGE_BUCKET_NAME = 'maxi-timeline-bucket'
AWS_S3_REGION_NAME = "eu-central-1"
AWS_DEFAULT_ACL = None
AWS_S3_SIGNATURE_VERSION = "s3v4"
AWS_S3_CUSTOM_DOMAIN = '%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME
AWS_S3_OBJECT_PARAMETERS = {
    'CacheControl': 'max-age=86400',
}
DEFAULT_FILE_STORAGE = 'timeline.storage_backends.MediaStorage'

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
WHITENOISE_ROOT = STATIC_ROOT
WHITENOISE_MAX_AGE = 31536000
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [STATIC_ROOT],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]
WSGI_APPLICATION = "timeline.wsgi.application"
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
    }
}
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]
LANGUAGE_CODE = "de-ch"
TIME_ZONE = "UTC"
USE_I18N = True
USE_L10N = True
USE_TZ = True

# https://github.com/jazzband/sorl-thumbnail#is-so-slow-in-amazon-s3
THUMBNAIL_FORCE_OVERWRITE = True

django_heroku.settings(locals(), logging=False)

try:
    from .local_settings import *
except:
    pass
