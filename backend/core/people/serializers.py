import os
from pathlib import Path

from core.image.models import Image
from core.image.serializers import ImageCreateSerializer
from core.image.serializers import ImageSerializer
from core.people import models
from django.conf import settings
from django.core.files import File
from django.core.files.images import get_image_dimensions
from rest_framework import serializers
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
        with open(image_path, "rb") as image:
            width, height = get_image_dimensions(image)
            person_image = Image.objects.create(title="title", person=person, width=width, height=height)
            person_image.file.save(file_name, File(image))
            os.remove(image_path)

    def to_representation(self, instance):
        return PersonSerializer(instance, context=self.context).data
