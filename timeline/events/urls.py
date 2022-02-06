from rest_framework import routers

from timeline.events.views import EventViewSet

router = routers.DefaultRouter()
router.register("", EventViewSet, basename="event")

urlpatterns = router.urls
