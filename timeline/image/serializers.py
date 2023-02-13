from rest_framework import serializers
from sorl.thumbnail import get_thumbnail as sorl_get_thumbnail

from timeline.image.models import Image


class ImageCreateSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    filename = serializers.CharField()


class ImageSerializer(serializers.ModelSerializer):
    dimensions = serializers.SerializerMethodField()
    thumbnail = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()

    class Meta:
        model = Image
        fields = ["id", "title", "description", "image", "dimensions", "thumbnail"]

    def get_dimensions(self, image):
        return {"width": image.width, "height": image.height}

    def get_thumbnail(self, image):
        thumbnail = sorl_get_thumbnail(image.file, "100x100", crop="center", quality=99)
        return self.context["request"].build_absolute_uri(thumbnail.url)

    def get_image(self, image):
        return self.context["request"].build_absolute_uri(image.file.url)
