from core.events.views import EventViewSet
from rest_framework import routers


router = routers.DefaultRouter()
router.register("", EventViewSet, basename="event")

urlpatterns = router.urls
