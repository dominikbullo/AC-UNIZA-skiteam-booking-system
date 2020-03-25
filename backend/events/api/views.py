from rest_framework import viewsets

from events.models import Event, Season
from events.api.serializers import EventPolymorphicSerializer, SeasonSerializer
from events.api.permissions import IsOwnerOrReadOnly, IsOwnFamilyOrReadOnly


# RES: https://github.com/LondonAppDeveloper/recipe-app-api/blob/master/app/recipe/views.py
# RES: https://stackoverflow.com/questions/51016896/how-to-serialize-inherited-models-in-django-rest-framework
class EventsViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventPolymorphicSerializer
    # permission_classes = [IsOwnFamilyOrReadOnly]
    # filter_backends = [SearchFilter]
    # search_fields = ["name"]


class CurrentSeasonEventsViewSet(viewsets.ModelViewSet):
    serializer_class = EventPolymorphicSerializer

    def get_queryset(self):
        return Event.objects.filter(season=Season.objects.get(current=True))


class SeasonViewSet(viewsets.ModelViewSet):
    queryset = Season.objects.all()
    serializer_class = SeasonSerializer
