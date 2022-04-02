from django_filters import rest_framework as filters
from rest_framework.mixins import RetrieveModelMixin
from rest_framework.viewsets import GenericViewSet, ModelViewSet

from timeline.events import models
from timeline.events.serializers import EventCreateOrUpdateSerializer, EventSerializer, ImageSerializer
from timeline.serializers import SerializerActionMixin



class EventFilter(filters.FilterSet):
    date = filters.DateFromToRangeFilter()
    title = filters.CharFilter(field_name="title", lookup_expr='icontains')

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


class ImageViewSet(RetrieveModelMixin, GenericViewSet):
    serializer_class = ImageSerializer
    queryset = models.Image.objects.all()
