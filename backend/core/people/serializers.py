import io
import os
from pathlib import Path

import pyvips
from django.conf import settings
from rest_framework import serializers

from core.image.models import Image
from core.image.serializers import ImageCreateSerializer, ImageSerializer
from core.people import models
from core.role.models import Role
from core.role.serializers import RoleSerializer


class PersonSerializer(serializers.ModelSerializer):
    image = ImageSerializer()
    role = RoleSerializer()

    class Meta:
        model = models.Person
        fields = (
            "id",
            "name",
            "role",
            "image",
        )


class PersonCreateOrUpdateSerializer(serializers.ModelSerializer):
    image = ImageCreateSerializer()
    role = serializers.PrimaryKeyRelatedField(queryset=Role.objects.all())

    class Meta:
        model = models.Person
        fields = ("id", "name", "role", "image")

    def save(self, *args, **kwargs):
        image = self.validated_data.pop("image")
        person = super().save(**kwargs)
        if "filename" not in image:
            return
        if hasattr(person, "image"):
            person.image.delete()
        file_name = image["filename"]
        image_path = Path(settings.TUS_DESTINATION_DIR) / file_name
        with pyvips.Image.new_from_file(image_path) as image:
            image = image.autorot()
            person_image = Image.objects.create(
                title="title",
                person=person,
                width=image.width,
                height=image.height,
            )
            person_image.file.save(
                file_name,
                io.BytesIO(image.write_to_buffer(".jpeg", **{"Q": 80, "strip": True})),
            )
            os.remove(image_path)

    def to_representation(self, instance):
        return PersonSerializer(instance, context=self.context).data
