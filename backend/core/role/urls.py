from rest_framework import routers

from core.role.views import RoleViewSet

router = routers.DefaultRouter()
router.register("", RoleViewSet, basename="role")

urlpatterns = router.urls
