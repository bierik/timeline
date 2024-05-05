from django_filters import rest_framework as filters
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from core.events import models
from core.events.pagination import CursorPagination
from core.events.serializers import (
    BulkCreateSerializer,
    EventCreateOrUpdateSerializer,
    EventSerializer,
)
from core.people.models import Person
from core.serializers import SerializerActionMixin


class AndModelMultipleChoiceFilter(filters.ModelMultipleChoiceFilter):
    def filter(self, qs, value):
        if value:
            qs = super().filter(qs, value)
            for val in value:
                qs = qs.filter(**{self.field_name: val})
        return qs


class EventFilter(filters.FilterSet):
    date = filters.DateFromToRangeFilter()
    title = filters.CharFilter(field_name="title", lookup_expr="icontains")
    people = AndModelMultipleChoiceFilter(queryset=Person.objects.all())

    class Meta:
        model = models.Event
        fields = ["date", "people"]


class EventViewSet(
    SerializerActionMixin,
    ModelViewSet,
):
    serializer_class = EventSerializer
    serializer_action_classes = {
        "create": EventCreateOrUpdateSerializer,
        "partial_update": EventCreateOrUpdateSerializer,
    }
    queryset = models.Event.objects.prefetch_related("images", "relations", "people").all()
    filter_backends = (filters.DjangoFilterBackend, OrderingFilter)
    filterset_class = EventFilter
    pagination_class = CursorPagination
    ordering = ("date",)

    @action(methods=["post"], detail=False)
    def bulk_create(self, request):
        serializer = BulkCreateSerializer(data=request.data, many=True)
        serializer.is_valid(raise_exception=True)

        for event_data in serializer.validated_data:
            images = event_data.pop("images", [])
            relations = event_data.pop("relations", [])
            people = event_data.pop("people", [])
            event = models.Event.objects.create(**event_data)
            event.relations.add(*relations)
            event.people.add(*people)
            for image_name in images:
                event.add_image(image_name)

        return Response()
