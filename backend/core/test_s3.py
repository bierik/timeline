import os

import requests
from botocore.exceptions import ClientError
from django.urls import reverse
from rest_framework import status

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
    data = build_random_string(data_size)
    key = f"test/{build_random_string(10).decode('utf-8')}.txt"
    return data, key


class S3MultipartUpload(TestCase):
    def test_make_chunks(self):
        with self.assertRaises(ValueError):
            parts, part_size = client.make_chunks(4 * MB)

        parts, part_size = client.make_chunks(5 * MB)
        self.assertEqual(1, len(parts))
        self.assertEqual(5 * MB, part_size)

        parts, part_size = client.make_chunks(6 * MB)
        self.assertEqual(1, len(parts))
        self.assertEqual(6 * MB, part_size)

        parts, part_size = client.make_chunks(49 * MB)
        self.assertEqual(1, len(parts))
        self.assertEqual(49 * MB, part_size)

        parts, part_size = client.make_chunks(50 * MB)
        self.assertEqual(1, len(parts))
        self.assertEqual(50 * MB, part_size)

        parts, part_size = client.make_chunks(51 * MB)
        self.assertEqual(2, len(parts))
        self.assertEqual(25.5 * MB, part_size)

        parts, part_size = client.make_chunks(99 * MB)
        self.assertEqual(2, len(parts))
        self.assertEqual(49.5 * MB, part_size)

        parts, part_size = client.make_chunks(100 * MB)
        self.assertEqual(2, len(parts))
        self.assertEqual(50 * MB, part_size)

        parts, part_size = client.make_chunks(101 * MB)
        self.assertEqual(3, len(parts))
        self.assertEqual(33666667, part_size)

    def test_uploads_files_in_multiple_parts(self):
        session = requests.Session()
        size = 51 * MB
        data, key = build_data(size)

        response = self.client.post(
            reverse("image_upload-start"),
            data={"key": key, "size": size},
            format="json",
        )
        self.assertEqual(status.HTTP_202_ACCEPTED, response.status_code, response.json())

        self.assertIn("upload_id", response.json())
        self.assertEqual(2, len(response.json()["parts"]))
        self.assertEqual(25.5 * MB, response.json()["part_size"])

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
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        response = client.client.get_object(Key=key, Bucket="test")
        self.assertEqual(51 * MB, response["ContentLength"])

    def test_falls_back_to_simple_upload_if_file_is_less_than_minium_chunk_size(self):
        session = requests.Session()
        size = 4 * MB
        data, key = build_data(size)

        response = self.client.post(
            reverse("image_upload-start"),
            data={"key": key, "size": size},
            format="json",
        )
        self.assertEqual(status.HTTP_202_ACCEPTED, response.status_code)

        self.assertEqual("multipart_fallback", response.json()["upload_id"])
        self.assertEqual(1, len(response.json()["parts"]))
        self.assertEqual(4 * MB, response.json()["part_size"])

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
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        response = client.client.get_object(Key=key, Bucket="test")
        self.assertEqual(4 * MB, response["ContentLength"])

    def test_abort_multi_part_upload(self):
        session = requests.Session()
        size = 51 * MB
        data, key = build_data(size)

        response = self.client.post(
            reverse("image_upload-start"),
            data={"key": key, "size": size},
            format="json",
        )
        self.assertEqual(status.HTTP_202_ACCEPTED, response.status_code)

        self.assertIn("upload_id", response.json())
        self.assertEqual(2, len(response.json()["parts"]))
        self.assertEqual(25.5 * MB, response.json()["part_size"])

        upload_info = response.json()
        uploaded_parts = []

        part_index = 0
        part = upload_info["parts"][0]
        part_start = part_index * upload_info["part_size"]
        part_end = part_start + upload_info["part_size"]
        response = session.put(part["url"], data=data[part_start:part_end], verify=False)
        uploaded_parts.append({"PartNumber": part["part_number"], "ETag": response.headers["ETag"]})

        response = self.client.post(
            reverse("image_upload-abort"),
            data={"key": key, "upload_id": upload_info["upload_id"]},
            format="json",
        )
        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)
        with self.assertRaisesMessage(ClientError, "The specified key does not exist."):
            client.client.get_object(Key=key, Bucket="test")

    def test_handles_abort_of_missing_upload(self):
        response = self.client.post(
            reverse("image_upload-abort"),
            data={"key": "missing", "upload_id": "something"},
            format="json",
        )
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        self.assertIn("An error occurred (NoSuchUpload)", response.json())

    def test_handles_end_upload_errors(self):
        response = self.client.post(
            reverse("image_upload-end"),
            data={"key": "missing", "upload_id": "something", "uploaded_parts": []},
            format="json",
        )
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        self.assertIn("An error occurred (InvalidRequest)", response.json())
