from core.role.views import RoleViewSet
from rest_framework import routers


router = routers.DefaultRouter()
router.register("", RoleViewSet, basename="role")

urlpatterns = router.urls
