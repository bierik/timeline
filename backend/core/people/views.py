from rest_framework.viewsets import ModelViewSet

from core.people import models
from core.people.serializers import PersonCreateOrUpdateSerializer, PersonSerializer
from core.serializers import SerializerActionMixin


class PersonViewSet(
    SerializerActionMixin,
    ModelViewSet,
):
    serializer_class = PersonSerializer
    serializer_action_classes = {
        "create": PersonCreateOrUpdateSerializer,
        "partial_update": PersonCreateOrUpdateSerializer,
    }
    queryset = models.Person.objects.select_related("image").all()
