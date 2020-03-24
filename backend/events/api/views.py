from rest_framework import viewsets

from events.models import SkiTraining, Event
from events.api.serializers import SkiTrainingSerializer, EventPolymorphicSerializer
from events.api.permissions import IsOwnerOrReadOnly, IsOwnFamilyOrReadOnly


# RES: https://github.com/LondonAppDeveloper/recipe-app-api/blob/master/app/recipe/views.py
# RES: https://stackoverflow.com/questions/51016896/how-to-serialize-inherited-models-in-django-rest-framework
class EventsViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventPolymorphicSerializer
    # permission_classes = [IsOwnFamilyOrReadOnly]
    # filter_backends = [SearchFilter]
    # search_fields = ["name"]


class SkiTrainingViewSet(viewsets.ModelViewSet):
    queryset = SkiTraining.objects.all()
    serializer_class = SkiTrainingSerializer
    # permission_classes = [IsOwnFamilyOrReadOnly]
    # filter_backends = [SearchFilter]
    # search_fields = ["name"]
