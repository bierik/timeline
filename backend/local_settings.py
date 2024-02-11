from pathlib import Path

from corsheaders.defaults import default_headers


BASE_DIR = Path(__file__).resolve().parent
ALLOWED_HOSTS = ["localhost"]
DEBUG = True
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": "timeline_development",
        "HOST": "localhost",
    }
}

SECURE_PROXY_SSL_HEADER = None
SECURE_SSL_REDIRECT = False

CORS_ALLOWED_ORIGINS = ["http://localhost:3000"]
CORS_ALLOW_HEADERS = default_headers + (
    "upload-offset",
    "upload-length",
    "upload-metadata",
    "tus-resumable",
    "tus-max-size",
    "tus-version",
)

STATIC_URL = "/staticfiles/"
STATIC_ROOT = BASE_DIR / "staticfiles"
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"
DEFAULT_FILE_STORAGE = "django.core.files.storage.FileSystemStorage"
