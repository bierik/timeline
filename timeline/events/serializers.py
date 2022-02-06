import os
from pathlib import Path

from django.conf import settings
from django.core.files import File
from django.core.files.images import get_image_dimensions
from django_editorjs_fields.templatetags.editorjs import editorjs
from rest_framework import serializers

from timeline.events import models


class ImageSerializer(serializers.ModelSerializer):
    dimensions = serializers.SerializerMethodField()

    class Meta:
        model = models.Image
        fields = ["id", "title", "description", "file", "dimensions"]

    def get_dimensions(self, image):
        width, height = get_image_dimensions(image.file)
        return {"width": width, "height": height}


class EventSerializer(serializers.ModelSerializer):
    start = serializers.DateField(source="date", read_only=True)
    images = ImageSerializer(read_only=True, many=True)
    has_images = serializers.SerializerMethodField()
    description_html = serializers.SerializerMethodField()

    class Meta:
        model = models.Event
        fields = (
            "id",
            "title",
            "description_html",
            "icon",
            "start",
            "images",
            "has_images",
        )

    def get_has_images(self, event):
        return event.images.exists()

    def get_description_html(self, event):
        return editorjs(event.description)


class EventCreateSerializer(serializers.ModelSerializer):
    files = serializers.ListField(child=serializers.CharField(), write_only=True)

    class Meta:
        model = models.Event
        fields = ("title", "description", "icon", "date", "files")

    def save(self, *args, **kwargs):
        files = self.validated_data.pop("files")
        event = super().save(**kwargs)
        for file in files:
            imagePath = Path(settings.TUS_DESTINATION_DIR) / file
            with open(imagePath, "rb") as image:
                event_image = models.Image.objects.create(title="title", event=event)
                event_image.file.save(file, File(image))
                os.remove(imagePath)
