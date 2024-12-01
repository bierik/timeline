import math
from functools import partial

from botocore.exceptions import ClientError
from django.conf import settings
from rest_framework import serializers, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from core.storage_backends import MediaStorage

MULTIPART_FALLBACK_UPLOAD_ID = "multipart_fallback"
UPLOAD_MIN_PART_SIZE = 5_000_000


def get_public_bucket_url(url):
    return url.replace(settings.S3_ENDPOINT_URL, settings.WEB_S3_ENDPOINT_URL)


class S3Client:
    def __init__(self):
        storage = MediaStorage()
        self.client = storage.connection.meta.client

    def make_chunks(self, size, max_chunk_size=50_000_000):
        if size < UPLOAD_MIN_PART_SIZE:
            raise ValueError("Minium size must be 5MB.")
        num_chunks = math.ceil(size / max_chunk_size)
        chunk_size = math.ceil(size / num_chunks)
        return range(1, num_chunks + 1), chunk_size

    def create_presigned_upload_part_url(self, key, upload_id, expires_in, part_number):
        url = self.client.generate_presigned_url(
            ClientMethod="upload_part",
            Params={
                "Bucket": settings.AWS_STORAGE_BUCKET_NAME,
                "Key": key,
                "PartNumber": part_number,
                "UploadId": upload_id,
            },
            ExpiresIn=expires_in,
            HttpMethod="PUT",
        )
        return {"part_number": part_number, "url": get_public_bucket_url(url)}

    def create_multipart_upload(self, key, size, acl="private", expiration=36000):
        multipart_upload = self.client.create_multipart_upload(Bucket=settings.AWS_STORAGE_BUCKET_NAME, Key=key, ACL=acl)
        upload_id = multipart_upload["UploadId"]
        parts, part_size = self.make_chunks(size)
        upload_parts = list(map(partial(self.create_presigned_upload_part_url, key, upload_id, expiration), parts))
        return upload_id, upload_parts, part_size


client = S3Client()


class S3StartMultipartRequestSerializer(serializers.Serializer):
    key = serializers.CharField()
    size = serializers.IntegerField()


class S3MultipartUploadedPartSerializer(serializers.Serializer):
    PartNumber = serializers.IntegerField()
    ETag = serializers.CharField()


class S3EndMultipartRequestSerializer(serializers.Serializer):
    key = serializers.CharField()
    upload_id = serializers.CharField()
    uploaded_parts = S3MultipartUploadedPartSerializer(many=True)


class S3AbortMultiPartRequestSerializer(serializers.Serializer):
    key = serializers.CharField()
    upload_id = serializers.CharField()


class S3MultipartUploadView(viewsets.GenericViewSet):
    def finish_upload(self, request):
        return Response(status=status.HTTP_204_NO_CONTENT)

    def validate_upload(self, request):
        pass

    @action(detail=False, methods=["POST"])
    def start(self, request):
        self.validate_upload(request)
        serializer = S3StartMultipartRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        if data["size"] >= UPLOAD_MIN_PART_SIZE:
            try:
                upload_id, upload_parts, part_size = client.create_multipart_upload(data["key"], data["size"])
                return Response(
                    data={"upload_id": upload_id, "parts": upload_parts, "part_size": part_size},
                    status=status.HTTP_202_ACCEPTED,
                )
            except ClientError as exc:
                return Response(str(exc), status=status.HTTP_400_BAD_REQUEST)
        else:
            try:
                url = client.client.generate_presigned_url(
                    ClientMethod="put_object",
                    Params={
                        "Bucket": settings.AWS_STORAGE_BUCKET_NAME,
                        "Key": data["key"],
                    },
                    HttpMethod="PUT",
                )
                return Response(
                    data={
                        "upload_id": MULTIPART_FALLBACK_UPLOAD_ID,
                        "parts": [{"part_number": 1, "url": get_public_bucket_url(url)}],
                        "part_size": data["size"],
                    },
                    status=status.HTTP_202_ACCEPTED,
                )
            except ClientError as exc:
                return Response(str(exc), status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=["POST"])
    def end(self, request):
        serializer = S3EndMultipartRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        if data["upload_id"] == MULTIPART_FALLBACK_UPLOAD_ID:
            return self.finish_upload(request)

        try:
            client.client.complete_multipart_upload(
                Bucket=settings.AWS_STORAGE_BUCKET_NAME,
                Key=data["key"],
                MultipartUpload={"Parts": data["uploaded_parts"]},
                UploadId=data["upload_id"],
            )
            return self.finish_upload(request)
        except ClientError as exc:
            return Response(str(exc), status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=["POST"])
    def abort(self, request):
        serializer = S3AbortMultiPartRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        try:
            client.client.abort_multipart_upload(
                Bucket=settings.AWS_STORAGE_BUCKET_NAME, Key=data["key"], UploadId=data["upload_id"]
            )
            return Response(status=status.HTTP_204_NO_CONTENT)
        except ClientError as exc:
            return Response(str(exc), status=status.HTTP_400_BAD_REQUEST)
