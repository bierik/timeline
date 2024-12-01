from core.s3 import S3MultipartUploadView


class ImageUploadViewSet(S3MultipartUploadView):
    def finish_upload(self, request):
        # key -> s3_path
        # event_id -> event_id
        return super().finish_upload(request)
