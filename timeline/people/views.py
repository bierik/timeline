from rest_framework.viewsets import ModelViewSet

from timeline.people import models
from timeline.people.serializers import PersonSerializer, PersonCreateOrUpdateSerializer
from timeline.serializers import SerializerActionMixin


class PersonViewSet(
    SerializerActionMixin, ModelViewSet,
):
    serializer_class = PersonSerializer
    serializer_action_classes = {"create": PersonCreateOrUpdateSerializer, "partial_update": PersonCreateOrUpdateSerializer}
    queryset = models.Person.objects.all()
