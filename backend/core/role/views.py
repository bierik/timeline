from core.role import models
from core.role.serializers import RoleSerializer
from rest_framework.viewsets import ModelViewSet


class RoleViewSet(ModelViewSet):
    serializer_class = RoleSerializer
    queryset = models.Role.objects.all()
