import pyvips
from django.contrib.auth import get_user_model
from django.core.files.base import ContentFile
from knox.models import AuthToken
from model_bakery import baker
from rest_framework.test import APITestCase

from timeline.image.models import Image


User = get_user_model()


class TestCase(APITestCase):
    def setUp(self):
        super().setUp()
        user = baker.make(User)
        _, token = AuthToken.objects.create(user=user)
        self.client.credentials(HTTP_AUTHORIZATION=("Token %s" % token))

    def create_image(self, **kwargs):
        image = pyvips.Image.black(100, 100)
        buf = image.write_to_buffer(".png")
        image = baker.make(Image, **kwargs)
        content_file = ContentFile(buf)
        image.file.save("test.jpeg", content_file)
        return image
