from django.urls import path, include
from rest_framework.routers import DefaultRouter

from events.api.views import EventsViewSet, CurrentSeasonEventsViewSet, SeasonViewSet, ChangeChildToEventAPIView

app_name = 'events'

# https://www.django-rest-framework.org/api-guide/routers/
router = DefaultRouter()
# TODO IDEA
# router.register(r"season/:id/events", CurrentSeasonEventsViewSet, basename="event")

router.register(r"season/events", CurrentSeasonEventsViewSet, basename="actual-season-event")
router.register(r"event", EventsViewSet, basename="event")
router.register(r"season", SeasonViewSet, basename="season")

urlpatterns = [
    path("", include(router.urls)),

    # TODO add event/:id/add-child/id -> then i can only add child to event no update
    path("event/<int:event_id>/change/", ChangeChildToEventAPIView.as_view()),
]
