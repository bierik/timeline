from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
ALLOWED_HOSTS = ["*"]
DEBUG = True

# SECURE_PROXY_SSL_HEADER = None
# SECURE_SSL_REDIRECT = False
USE_X_FORWARDED_HOST = True

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"
DEFAULT_FILE_STORAGE = "django.core.files.storage.FileSystemStorage"

LOGGING = None
