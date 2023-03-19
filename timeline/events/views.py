from django_filters import rest_framework as filters
from rest_framework.filters import OrderingFilter
from rest_framework.viewsets import ModelViewSet

from timeline.events import models
from timeline.events.pagination import CursorPagination
from timeline.events.serializers import EventCreateOrUpdateSerializer, EventSerializer
from timeline.serializers import SerializerActionMixin


class EventFilter(filters.FilterSet):
    date = filters.DateFromToRangeFilter()
    title = filters.CharFilter(field_name="title", lookup_expr="icontains")

    class Meta:
        model = models.Event
        fields = ["date"]


class EventViewSet(
    SerializerActionMixin,
    ModelViewSet,
):
    serializer_class = EventSerializer
    serializer_action_classes = {
        "create": EventCreateOrUpdateSerializer,
        "partial_update": EventCreateOrUpdateSerializer,
    }
    queryset = models.Event.objects.all()
    filter_backends = (filters.DjangoFilterBackend, OrderingFilter)
    filterset_class = EventFilter
    pagination_class = CursorPagination
    ordering = ("date",)
