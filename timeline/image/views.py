from rest_framework.mixins import RetrieveModelMixin
from rest_framework.viewsets import GenericViewSet

from timeline.events import models
from timeline.image.serializers import ImageSerializer

class ImageViewSet(RetrieveModelMixin, GenericViewSet):
    serializer_class = ImageSerializer
    queryset = models.Image.objects.all()
