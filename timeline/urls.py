from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path, re_path
from django_tus.views import TusUpload
from django.views.generic import TemplateView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("timeline.events.urls")),
    path("api/upload/", TusUpload.as_view(), name="tus_upload"),
    path(
        "api/upload/<uuid:resource_id>", TusUpload.as_view(), name="tus_upload_chunks"
    ),
    path('editorjs/', include('django_editorjs_fields.urls')),
    re_path(r'', TemplateView.as_view(template_name='index.html')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
