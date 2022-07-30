import os
from pathlib import Path

from django.conf import settings
from django.core.files import File
from django.core.files.images import get_image_dimensions
from django_editorjs_fields.templatetags.editorjs import editorjs
from rest_framework import serializers

from timeline.events import models
from sorl.thumbnail import get_thumbnail as sorl_get_thumbnail
from rest_framework_recursive.fields import RecursiveField


class ImageSerializer(serializers.ModelSerializer):
    dimensions = serializers.SerializerMethodField()
    thumbnail = serializers.SerializerMethodField()
    file = serializers.SerializerMethodField()

    class Meta:
        model = models.Image
        fields = ["id", "title", "description", "file", "dimensions", "thumbnail"]

    def get_dimensions(self, image):
        return {"width": image.width, "height": image.height}

    def get_thumbnail(self, image):
        thumbnail = sorl_get_thumbnail(image.file, '100x100', crop='center', quality=99)
        return self.context["request"].build_absolute_uri(thumbnail.url)

    def get_file(self, image):
        return self.context["request"].build_absolute_uri(image.file.url)



class EventSerializer(serializers.ModelSerializer):
    start = serializers.DateField(source="date", read_only=True)
    images = ImageSerializer(read_only=True, many=True)
    has_images = serializers.SerializerMethodField()
    description_html = serializers.SerializerMethodField()
    relations = RecursiveField(many=True)
    thumbnail = serializers.SerializerMethodField()

    class Meta:
        model = models.Event
        fields = (
            "id",
            "title",
            "description_html",
            "description",
            "icon",
            "start",
            "date",
            "images",
            "has_images",
            "relations",
            "thumbnail",
        )

    def get_has_images(self, event):
        return event.images.exists()

    def get_description_html(self, event):
        return editorjs(event.description)

    def get_thumbnail(self, event):
        if event.images.exists():
            thumbnail = sorl_get_thumbnail(event.images.first().file, '100x100', crop="center")
            return self.context["request"].build_absolute_uri(thumbnail.url)
        return None

class EventCreateOrUpdateSerializer(serializers.ModelSerializer):
    files = serializers.ListField(child=serializers.CharField(), write_only=True)
    deleted_files = serializers.ListField(child=serializers.IntegerField(), write_only=True, required=False)

    class Meta:
        model = models.Event
        fields = ("id", "title", "description", "icon", "date", "files", "deleted_files", "relations")

    def save(self, *args, **kwargs):
        deleted_files = self.validated_data.pop("deleted_files", [])
        files = self.validated_data.pop("files")

        event = super().save(**kwargs)
        for file in files:
            imagePath = Path(settings.TUS_DESTINATION_DIR) / file
            with open(imagePath, "rb") as image:
                width, height = get_image_dimensions(image)
                event_image = models.Image.objects.create(title="title", event=event, width=width, height=height)
                event_image.file.save(file, File(image))
                os.remove(imagePath)

        models.Image.objects.filter(id__in=deleted_files).delete()
