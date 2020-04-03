from django.urls import path, include
from rest_framework.routers import DefaultRouter

from events.api.views import EventViewSet, CurrentSeasonEventViewSet, SeasonViewSet, ChangeChildToEventAPIView

app_name = 'events'

# https://www.django-rest-framework.org/api-guide/routers/
router = DefaultRouter()

router.register(r"season/event", CurrentSeasonEventViewSet, basename="actual-season-event")
router.register(r"event", EventViewSet, basename="event")
router.register(r"season", SeasonViewSet, basename="season")

urlpatterns = [
    path("", include(router.urls)),
    path("event/<int:event_id>/change/", ChangeChildToEventAPIView.as_view()),
]
