import os
from pathlib import Path

from django.conf import settings
from django.core.files import File
from django.core.files.images import get_image_dimensions
from rest_framework import serializers

from timeline.people import models

from timeline.image.serializers import ImageSerializer
from timeline.image.models import Image


class PersonSerializer(serializers.ModelSerializer):
    image = ImageSerializer(read_only=True)
    role_display = serializers.CharField(source="get_role_display", read_only=True)

    class Meta:
        model = models.Person
        fields = (
            "id",
            "name",
            "role",
            "role_display",
            "image",
        )


class PersonCreateOrUpdateSerializer(serializers.ModelSerializer):
    file = serializers.CharField(write_only=True)

    class Meta:
        model = models.Person
        fields = ("id", "name", "role", "file")

    def save(self, *args, **kwargs):
        file = self.validated_data.pop("file")

        person = super().save(**kwargs)
        imagePath = Path(settings.TUS_DESTINATION_DIR) / file
        with open(imagePath, "rb") as image:
            width, height = get_image_dimensions(image)
            person_image = Image.objects.create(title="title", person=person, width=width, height=height)
            person_image.file.save(file, File(image))
            os.remove(imagePath)
