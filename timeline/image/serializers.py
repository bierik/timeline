from rest_framework import serializers
from timeline.image.models import Image
from sorl.thumbnail import get_thumbnail as sorl_get_thumbnail

class ImageSerializer(serializers.ModelSerializer):
    dimensions = serializers.SerializerMethodField()
    thumbnail = serializers.SerializerMethodField()
    file = serializers.SerializerMethodField()

    class Meta:
        model = Image
        fields = ["id", "title", "description", "file", "dimensions", "thumbnail"]

    def get_dimensions(self, image):
        return {"width": image.width, "height": image.height}

    def get_thumbnail(self, image):
        thumbnail = sorl_get_thumbnail(image.file, '100x100', crop='center', quality=99)
        return self.context["request"].build_absolute_uri(thumbnail.url)

    def get_file(self, image):
        return self.context["request"].build_absolute_uri(image.file.url)
