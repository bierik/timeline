from pathlib import Path

from rest_framework.response import Response

from core.image.models import Image
from core.s3 import S3MultipartUploadView


def build_prefix(image, key):
    suffix = Path(key).suffix
    prefix = Path(str(image.pk))
    return str((prefix / "original").with_suffix(suffix))


class ImageUploadViewSet(S3MultipartUploadView):
    def finish_upload(self, request):
        image = Image.objects.create()
        image.file.name = build_prefix(image, request.data["key"])
        image.save()
        return Response({"id": image.pk})
