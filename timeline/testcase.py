import io
import os

from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase as DjangoTestCase
from model_bakery import baker
from PIL import Image as PILImage
from rest_framework.test import APIClient

from timeline.image.models import Image


class TestCase(DjangoTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.snapshot_before = cls.filestructure_snapshot(settings.MEDIA_ROOT)
        cls.client = APIClient()

    def tearDown(self):
        snapshot_after = self.filestructure_snapshot(settings.MEDIA_ROOT)
        self.delete_snapshot_difference(snapshot_after, self.snapshot_before)

    @staticmethod
    def filestructure_snapshot(path):
        paths = []
        for dirpath, _dirnames, filenames in os.walk(path):
            paths.append(dirpath)
            for filename in filenames:
                paths.append(os.path.join(dirpath, filename))
        return paths

    @staticmethod
    def delete_snapshot_difference(snapshot_after, snapshot_before):
        to_delete = reversed(sorted(set(snapshot_after) - set(snapshot_before)))
        for path in to_delete:
            if os.path.isfile(path):
                os.unlink(path)
            if os.path.isdir(path):
                os.removedirs(path)

    def create_image(self, format="JPEG", **kwargs):
        with io.BytesIO() as output:
            PILImage.new("RGB", (100, 100), color="black").save(output, format=format)
            image = baker.make(Image, **kwargs)
            image.file.save("test.jpeg", output)
        return image

    def create_uploaded_image(self):
        with io.BytesIO() as output:
            PILImage.new("RGB", (100, 100), color="black").save(output, format=format)
            image = SimpleUploadedFile("test.jpeg", output, content_type="image/jpeg")
        return image
