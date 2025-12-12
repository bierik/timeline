from django.contrib import admin
from django.urls import include, path
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
    path("api/auth/", include("core.authentication.urls")),
]
