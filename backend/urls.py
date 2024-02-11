from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include
from django.urls import path
from django.urls import re_path
from django.views.generic import TemplateView
from django_tus.views import TusUpload


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/events/", include("core.events.urls")),
    path("api/people/", include("core.people.urls")),
    path("api/upload/", TusUpload.as_view(), name="tus_upload"),
    path("api/upload/<uuid:resource_id>", TusUpload.as_view(), name="tus_upload_chunks"),
    path("editorjs/", include("django_editorjs_fields.urls")),
    path("api/auth/", include("core.authentication.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
else:
    urlpatterns += [re_path(r"", TemplateView.as_view(template_name="index.html"))]
