from core.people.views import PersonViewSet
from rest_framework import routers


router = routers.DefaultRouter()
router.register("", PersonViewSet, basename="person")

urlpatterns = router.urls
