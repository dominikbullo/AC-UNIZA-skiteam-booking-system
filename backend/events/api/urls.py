from django.urls import path, include
from rest_framework.routers import DefaultRouter

from events.api.views import EventViewSet, SeasonViewSet

app_name = 'events'

# https://www.django-rest-framework.org/api-guide/routers/
router = DefaultRouter()

router.register(r"event", EventViewSet, basename="event")
router.register(r"season", SeasonViewSet, basename="season")

urlpatterns = [
    path("", include(router.urls)),
]
