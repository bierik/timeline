import os

import requests
from django.urls import reverse

from core.image.models import Image
from core.s3 import S3Client
from core.testcase import TestCase

MB = 1_000_000

client = S3Client()


def build_random_string(size):
    min_lc = ord(b"a")
    len_lc = 26
    ba = bytearray(os.urandom(int(size)))
    for i, b in enumerate(ba):
        ba[i] = min_lc + b % len_lc  # convert 0..255 to 97..122
    return ba


def build_data(size):
    data_size = size
    return build_random_string(data_size)


class ImageUploadTestCase(TestCase):
    def test_creates_image_object_when_upload_completes(self):
        session = requests.Session()
        size = 51 * MB
        data = build_data(size)
        key = "test.txt"

        response = self.client.post(
            reverse("image_upload-start"),
            data={"key": key, "size": size},
            format="json",
        )
        upload_info = response.json()
        uploaded_parts = []

        for part_index, part in enumerate(upload_info["parts"]):
            part_start = part_index * upload_info["part_size"]
            part_end = part_start + upload_info["part_size"]
            response = session.put(part["url"], data=data[part_start:part_end], verify=False)
            uploaded_parts.append({"PartNumber": part["part_number"], "ETag": response.headers["ETag"]})

        response = self.client.post(
            reverse("image_upload-end"),
            data={
                "key": key,
                "upload_id": upload_info["upload_id"],
                "uploaded_parts": uploaded_parts,
            },
            format="json",
        )
        self.assertEqual({"id": Image.objects.first().pk}, response.json())
        self.assertEqual(["1/original.txt"], list(Image.objects.values_list("file", flat=True)))
