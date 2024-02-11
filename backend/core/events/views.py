import io
import os
from pathlib import Path

import pyvips
from core.events import models
from core.events.pagination import CursorPagination
from core.events.serializers import BulkCreateSerializer
from core.events.serializers import EventCreateOrUpdateSerializer
from core.events.serializers import EventSerializer
from core.image.models import Image
from core.people.models import Person
from core.serializers import SerializerActionMixin
from django.conf import settings
from django_filters import rest_framework as filters
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

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
    queryset = models.Event.objects.all()
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
            event = models.Event.objects.create(**event_data)
            for image_name in images:
                imagePath = Path(settings.TUS_DESTINATION_DIR) / image_name
                with pyvips.Image.new_from_file(imagePath) as image:
                    image = image.autorot()
                    event_image = Image.objects.create(title="title", event=event, width=image.width, height=image.height)
                    event_image.file.save(image_name, io.BytesIO(image.write_to_buffer(".jpeg")))
                    os.remove(imagePath)

        return Response()
