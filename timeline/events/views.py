import os
from pathlib import Path

from django.conf import settings
from django.core.files import File
from django.core.files.images import get_image_dimensions
from django_filters import rest_framework as filters
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from timeline.events import models
from timeline.events.pagination import CursorPagination
from timeline.events.serializers import BulkCreateSerializer
from timeline.events.serializers import EventCreateOrUpdateSerializer
from timeline.events.serializers import EventSerializer
from timeline.image.models import Image
from timeline.serializers import SerializerActionMixin


class EventFilter(filters.FilterSet):
    date = filters.DateFromToRangeFilter()
    title = filters.CharFilter(field_name="title", lookup_expr="icontains")

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
                with open(imagePath, "rb") as image:
                    width, height = get_image_dimensions(image)
                    event_image = Image.objects.create(title="title", event=event, width=width, height=height)
                    event_image.file.save(image_name, File(image))
                    os.remove(imagePath)

        return Response()
