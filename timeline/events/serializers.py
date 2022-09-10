import os
from pathlib import Path

from django.conf import settings
from django.core.files import File
from django.core.files.images import get_image_dimensions
from django_editorjs_fields.templatetags.editorjs import editorjs
from rest_framework import serializers

from timeline.events import models
from sorl.thumbnail import get_thumbnail as sorl_get_thumbnail

from timeline.image.serializers import ImageSerializer
from timeline.image.models import Image
from timeline.people.serializers import PersonSerializer




class EventRelatedSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Event
        fields = ("id", "title")


class EventSerializer(serializers.ModelSerializer):
    start = serializers.DateField(source="date", read_only=True)
    images = ImageSerializer(read_only=True, many=True)
    has_images = serializers.SerializerMethodField()
    description_html = serializers.SerializerMethodField()
    relations = serializers.SerializerMethodField()
    thumbnail = serializers.SerializerMethodField()
    people = PersonSerializer(read_only=True, many=True)

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
            "people",
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

    def get_relations(self, event):
        relations = event.relations.values_list('id', flat=True)
        reverse_relations = event.reverse_relations.values_list('id', flat=True)
        return EventRelatedSerializer(models.Event.objects.filter(id__in=[*relations, *reverse_relations]), many=True).data


class EventCreateOrUpdateSerializer(serializers.ModelSerializer):
    files = serializers.ListField(child=serializers.CharField(), write_only=True)
    deleted_files = serializers.ListField(child=serializers.IntegerField(), write_only=True, required=False)

    class Meta:
        model = models.Event
        fields = ("id", "title", "description", "icon", "date", "files", "deleted_files", "relations", "people")

    def save(self, *args, **kwargs):
        deleted_files = self.validated_data.pop("deleted_files", [])
        files = self.validated_data.pop("files")

        event = super().save(**kwargs)
        for file in files:
            imagePath = Path(settings.TUS_DESTINATION_DIR) / file
            with open(imagePath, "rb") as image:
                width, height = get_image_dimensions(image)
                event_image = Image.objects.create(title="title", event=event, width=width, height=height)
                event_image.file.save(file, File(image))
                os.remove(imagePath)

        Image.objects.filter(id__in=deleted_files).delete()
