from django.urls import path, include
from rest_framework.routers import DefaultRouter

from events.api.views import EventsViewSet, SkiTrainingViewSet

app_name = 'events'

# https://www.django-rest-framework.org/api-guide/routers/
router = DefaultRouter()
router.register(r"events", EventsViewSet, basename="event")
router.register(r"trainings", SkiTrainingViewSet, basename="ski-training")

urlpatterns = [
    path("", include(router.urls)),
]
