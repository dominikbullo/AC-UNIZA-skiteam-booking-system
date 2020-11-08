from django.urls import path, include
from rest_framework.routers import DefaultRouter

from apps.events.api.views import (EventViewSet, SeasonViewSet, CategoryViewSet, LocationViewSet, RaceOrganizerViewSet,
                                   EventTypeViewSet, SkisTypeViewSet, AccommodationViewSet)

app_name = 'events'

# https://www.django-rest-framework.org/api-guide/routers/
router = DefaultRouter()

router.register(r"events?", EventViewSet, basename="event")
router.register(r"event-types?", EventTypeViewSet, basename="event-type")

router.register(r"seasons?", SeasonViewSet, basename="season")
router.register(r"locations?", LocationViewSet, basename="location")
router.register(r"skis-types?", SkisTypeViewSet, basename="skis-type")

router.register(r"race-organizers?", RaceOrganizerViewSet, basename="race-organizer")
router.register(r"accommodations?", AccommodationViewSet, basename="accommodation")

router.register(r"categories", CategoryViewSet, basename="categories")
router.register(r"category", CategoryViewSet, basename="category")

urlpatterns = [
]
