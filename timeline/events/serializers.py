from rest_framework import serializers
from timeline.events import models
from django.core.files.images import get_image_dimensions


class ImageSerializer(serializers.ModelSerializer):
    dimensions = serializers.SerializerMethodField()

    class Meta:
        model = models.Image
        fields = ["id", "title", "description", "file", "dimensions"]

    def get_dimensions(self, image):
        width, height = get_image_dimensions(image.file)
        return {"width":width, "height":height}


class EventSerializer(serializers.ModelSerializer):
    start = serializers.DateField(source="date", read_only=True)
    images = ImageSerializer(read_only=True, many=True)
    has_images = serializers.SerializerMethodField()

    class Meta:
        model = models.Event
        fields = ("id", "title", "description", "icon", "date", "start", "images", "has_images")
        write_only_fields = ("date",)
        read_only_fields = ("start",) 

    def get_has_images(self, event):
        return event.images.exists()
