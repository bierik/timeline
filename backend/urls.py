from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django_tus.views import TusUpload
from rest_framework import routers

from core.image.views import ImageUploadViewSet

router = routers.DefaultRouter()
router.register("upload", ImageUploadViewSet, basename="image_upload")


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/events/", include("core.events.urls")),
    path("api/people/", include("core.people.urls")),
    path("api/roles/", include("core.role.urls")),
    *router.urls,
    path("api/upload/", TusUpload.as_view(), name="tus_upload"),
    path("api/upload/<uuid:resource_id>", TusUpload.as_view(), name="tus_upload_chunks"),
    path("api/auth/", include("core.authentication.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
