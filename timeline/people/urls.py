from rest_framework import routers

from timeline.people.views import PersonViewSet


router = routers.DefaultRouter()
router.register("", PersonViewSet, basename="person")

urlpatterns = router.urls
