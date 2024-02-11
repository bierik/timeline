from core.people import models
from core.people.serializers import PersonCreateOrUpdateSerializer
from core.people.serializers import PersonSerializer
from core.serializers import SerializerActionMixin
from rest_framework.viewsets import ModelViewSet


class PersonViewSet(
    SerializerActionMixin,
    ModelViewSet,
):
    serializer_class = PersonSerializer
    serializer_action_classes = {
        "create": PersonCreateOrUpdateSerializer,
        "partial_update": PersonCreateOrUpdateSerializer,
    }
    queryset = models.Person.objects.all()
