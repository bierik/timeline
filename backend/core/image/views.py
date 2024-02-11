from core.events import models
from core.image.serializers import ImageSerializer
from rest_framework.mixins import RetrieveModelMixin
from rest_framework.viewsets import GenericViewSet


class ImageViewSet(RetrieveModelMixin, GenericViewSet):
    serializer_class = ImageSerializer
    queryset = models.Image.objects.all()
