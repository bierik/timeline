import os
import sys
from pathlib import Path

from configurations import Configuration, values


class Base(Configuration):
    BASE_DIR = Path(__file__).resolve().parent
    SECRET_KEY = values.Value("django-insecure-4t0+fq(6892+u&3s=gv48=)9487&oi6e=s&%pn00)-kj^i5g_#")
    ALLOWED_HOSTS = ["maxi-timeline.app"]
    INSTALLED_APPS = [
        "django.contrib.admin",
        "django.contrib.auth",
        "django.contrib.contenttypes",
        "django.contrib.sessions",
        "django.contrib.messages",
        "django.contrib.staticfiles",
        "django_extensions",
        "django_filters",
        "rest_framework",
        "knox",
        "django_tus",
        "sorl.thumbnail",
        "core",
        "django_cleanup.apps.CleanupConfig",
    ]
    MIDDLEWARE = [
        "django.middleware.security.SecurityMiddleware",
        "django.contrib.sessions.middleware.SessionMiddleware",
        "django.middleware.common.CommonMiddleware",
        "django.middleware.csrf.CsrfViewMiddleware",
        "django.contrib.auth.middleware.AuthenticationMiddleware",
        "django.contrib.messages.middleware.MessageMiddleware",
        "django.middleware.clickjacking.XFrameOptionsMiddleware",
    ]
    ROOT_URLCONF = "urls"

    ATOMIC_REQUESTS = True

    DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
    DATA_UPLOAD_MAX_MEMORY_SIZE = 5242880
    TUS_UPLOAD_DIR = BASE_DIR / "tus/tus_intermediate"
    TUS_DESTINATION_DIR = BASE_DIR / "tus/tus_destination"
    TUS_FILE_NAME_FORMAT = "keep"
    TUS_EXISTING_FILE = "error"

    SILENCED_SYSTEM_CHECKS = ["rest_framework.W001"]

    REST_FRAMEWORK = {
        "PAGE_SIZE": 10,
        "DEFAULT_AUTHENTICATION_CLASSES": [
            "knox.auth.TokenAuthentication",
        ],
        "DEFAULT_PERMISSION_CLASSES": [
            "rest_framework.permissions.IsAuthenticated",
        ],
    }

    AWS_STORAGE_BUCKET_NAME = "maxi-timeline-bucket"
    AWS_S3_REGION_NAME = "eu-central-1"
    AWS_DEFAULT_ACL = None
    AWS_S3_SIGNATURE_VERSION = "s3v4"
    AWS_S3_CUSTOM_DOMAIN = f"{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com"
    AWS_S3_OBJECT_PARAMETERS = {
        "CacheControl": "max-age=31536000",
    }
    STORAGES = {
        "default": {
            "BACKEND": "core.storage_backends.MediaStorage",
        },
        "staticfiles": {
            "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
        },
    }

    STATIC_URL = "/static/"
    STATIC_ROOT = BASE_DIR / "staticfiles"
    TEMPLATES = [
        {
            "BACKEND": "django.template.backends.django.DjangoTemplates",
            "DIRS": [STATIC_ROOT],
            "APP_DIRS": True,
            "OPTIONS": {
                "context_processors": [
                    "django.template.context_processors.request",
                    "django.contrib.auth.context_processors.auth",
                    "django.contrib.messages.context_processors.messages",
                ],
            },
        },
    ]
    WSGI_APPLICATION = "wsgi.application"

    @property
    def DATABASES(self):  # noqa: N802
        options = {}
        if os.environ.get("DJANGO_DATABASE_REQUIRE_SSL", False):
            options["sslmode"] = "require"
        config = {
            "ENGINE": "django.db.backends.postgresql_psycopg2",
            "NAME": os.environ.get("DJANGO_DATABASE_NAME", "postgres"),
            "HOST": os.environ.get("DJANGO_DATABASE_HOST", "db"),
            "USER": os.environ.get("DJANGO_DATABASE_USER", "postgres"),
            "PASSWORD": os.environ.get("DJANGO_DATABASE_PASSWORD", "postgres"),
            "PORT": os.environ.get("DJANGO_DATABASE_PORT", "5432"),
            "ATOMIC_REQUESTS": True,
            "OPTIONS": options,
        }
        return {"default": config}

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

    REST_KNOX = {
        "TOKEN_TTL": None,
        "USER_SERIALIZER": "core.authentication.serializers.UserSerializer",
    }
    AUTH_USER_MODEL = "core.User"

    LOGGING = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "verbose": {
                "format": "{asctime} {levelname} {name} {message}",
                "style": "{",
            },
        },
        "handlers": {
            "console": {
                "level": "ERROR",
                "class": "logging.StreamHandler",
                "formatter": "verbose",
                "stream": sys.stderr,
            },
        },
        "loggers": {
            "": {
                "handlers": ["console"],
                "level": "WARNING",
            },
            "django": {
                "handlers": ["console"],
                "level": "WARNING",
                "propagate": False,
            },
        },
    }


class Prod(Base):
    pass


class Dev(Base):
    ALLOWED_HOSTS = ["*"]
    DEBUG = True
    USE_X_FORWARDED_HOST = True
    MEDIA_URL = "/media/"

    @property
    def MEDIA_ROOT(self):  # noqa: N802
        return self.BASE_DIR / "media"

    STORAGES = {
        "default": {
            "BACKEND": "django.core.files.storage.FileSystemStorage",
        },
        "staticfiles": {
            "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
        },
    }
    LOGGING = None
