import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")
os.environ.setdefault("DJANGO_CONFIGURATION", "Prod")

from configurations.wsgi import get_wsgi_application  # noqa: E402

application = get_wsgi_application()
