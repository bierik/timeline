import os
from pathlib import Path

from django.conf import settings
from django.core.files import File
from django.core.files.images import get_image_dimensions
from rest_framework import serializers

from timeline.image.models import Image
from timeline.image.serializers import ImageSerializer
from timeline.people import models


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


class FileCreateSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    file = serializers.CharField()


class PersonCreateOrUpdateSerializer(serializers.ModelSerializer):
    image = FileCreateSerializer()

    class Meta:
        model = models.Person
        fields = ("id", "name", "role", "image")

    def save(self, *args, **kwargs):
        file = self.validated_data.pop("image")

        person = super().save(**kwargs)
        imagePath = Path(settings.TUS_DESTINATION_DIR) / file['file']
        with open(imagePath, "rb") as image:
            width, height = get_image_dimensions(image)
            person_image = Image.objects.create(title="title", person=person, width=width, height=height)
            person_image.file.save(file['file'], File(image))
            os.remove(imagePath)

    def to_representation(self, instance):
        return PersonSerializer(instance, context=self.context).data
