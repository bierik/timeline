from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import ListModelMixin
from rest_framework.mixins import CreateModelMixin
from timeline.events.serializers import EventSerializer
from timeline.events import models
from django_filters import rest_framework as filters


class EventFilter(filters.FilterSet):
    date = filters.DateFromToRangeFilter()

    class Meta:
        model = models.Event
        fields = ['date']

class EventViewSet(ListModelMixin, CreateModelMixin, GenericViewSet):
    serializer_class = EventSerializer
    queryset = models.Event.objects.all()
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = EventFilter

