import os
from operator import itemgetter
from pathlib import Path

from django.conf import settings
from django.core.files import File
from django.core.files.images import get_image_dimensions
from django_editorjs_fields.templatetags.editorjs import editorjs
from rest_framework import serializers
from sorl.thumbnail import get_thumbnail as sorl_get_thumbnail

from timeline.events import models
from timeline.image.models import Image
from timeline.image.serializers import ImageCreateSerializer, ImageSerializer
from timeline.people.serializers import PersonSerializer


class EventRelatedSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Event
        fields = ("id", "title")


class EventSerializer(serializers.ModelSerializer):
    start = serializers.DateField(source="date")
    images = ImageSerializer(many=True)
    has_images = serializers.SerializerMethodField()
    description_html = serializers.SerializerMethodField()
    relations = serializers.SerializerMethodField()
    thumbnail = serializers.SerializerMethodField()
    people = PersonSerializer(many=True)

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
            thumbnail = sorl_get_thumbnail(
                event.images.first().file, "100x100", crop="center"
            )
            return self.context["request"].build_absolute_uri(thumbnail.url)
        return None

    def get_relations(self, event):
        relations = event.relations.values_list("id", flat=True)
        reverse_relations = event.reverse_relations.values_list("id", flat=True)
        return EventRelatedSerializer(
            models.Event.objects.filter(id__in=[*relations, *reverse_relations]),
            many=True,
        ).data


class EventCreateOrUpdateSerializer(serializers.ModelSerializer):
    images = ImageCreateSerializer(many=True)

    class Meta:
        model = models.Event
        fields = (
            "id",
            "title",
            "description",
            "icon",
            "date",
            "images",
            "relations",
            "people",
        )

    def save(self, *args, **kwargs):
        images = self.validated_data.pop("images")
        event = super().save(**kwargs)

        event.images.exclude(id__in=map(itemgetter("id"), images)).delete()
        existing_image_ids = list(event.images.values_list("id", flat=True))

        new_images = list(
            filter(lambda image: image["id"] not in existing_image_ids, images)
        )
        for file_name in map(itemgetter("filename"), new_images):
            imagePath = Path(settings.TUS_DESTINATION_DIR) / file_name
            with open(imagePath, "rb") as image:
                width, height = get_image_dimensions(image)
                event_image = Image.objects.create(
                    title="title", event=event, width=width, height=height
                )
                event_image.file.save(file_name, File(image))
                os.remove(imagePath)

    def to_representation(self, instance):
        return EventSerializer(instance, context=self.context).data
