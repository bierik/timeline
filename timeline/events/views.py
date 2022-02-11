from django.http.response import HttpResponse
from django_filters import rest_framework as filters
from PIL import Image
from rest_framework.decorators import action
from rest_framework.mixins import CreateModelMixin, ListModelMixin, RetrieveModelMixin, UpdateModelMixin
from rest_framework.viewsets import GenericViewSet, ModelViewSet

from timeline.events import models
from timeline.events.serializers import EventCreateOrUpdateSerializer, EventSerializer, ImageSerializer
from timeline.serializers import SerializerActionMixin


class EventFilter(filters.FilterSet):
    date = filters.DateFromToRangeFilter()

    class Meta:
        model = models.Event
        fields = ["date"]


class EventViewSet(
    SerializerActionMixin, ModelViewSet,
):
    serializer_class = EventSerializer
    serializer_action_classes = {"create": EventCreateOrUpdateSerializer, "partial_update": EventCreateOrUpdateSerializer}
    queryset = models.Event.objects.all()
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = EventFilter

    @action(methods=["GET"], detail=True)
    def thumbnail(self, _, pk=None):
        event = models.Event.objects.get(pk=pk)
        image = Image.open(event.images.first().file)
        image.thumbnail((100, 100), Image.ANTIALIAS)
        response = HttpResponse(content_type="image/jpeg")
        image.save(response, "jpeg")
        return response


class ImageViewSet(RetrieveModelMixin, GenericViewSet):
    serializer_class = ImageSerializer
    queryset = models.Image.objects.all()
