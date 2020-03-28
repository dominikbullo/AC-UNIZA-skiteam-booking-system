from django.http import Http404
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.views import APIView

from events.models import Event, Season
from events.api.serializers import EventPolymorphicSerializer, SeasonSerializer
from events.api.permissions import IsOwnerOrReadOnly, IsOwnFamilyOrReadOnly

# RES: https://github.com/LondonAppDeveloper/recipe-app-api/blob/master/app/recipe/views.py
# RES: https://stackoverflow.com/questions/51016896/how-to-serialize-inherited-models-in-django-rest-framework
from family.api.serializers import ChildSerializer, ChildProfileSerializer
from family.models import Child
from users.models import User


class EventsViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventPolymorphicSerializer

    # permission_classes = [IsOwnFamilyOrReadOnly]
    # filter_backends = [SearchFilter]
    # search_fields = ["name"]


class CurrentSeasonEventsViewSet(EventsViewSet):
    serializer_class = EventPolymorphicSerializer

    def get_queryset(self):
        return Event.objects.filter(season=Season.objects.get(current=True))


class AddChildToEventAPIView(APIView):

    def get_event(self, pk):
        return get_object_or_404(Event, pk=pk)

    def get_child(self, username):
        return get_object_or_404(Child, user=User.objects.get(username=username))

    def get(self, request, event_id):
        return Response(status=status.HTTP_204_NO_CONTENT)

    def post(self, request, event_id):
        event = self.get_event(event_id)
        event_serializer = EventPolymorphicSerializer(event)
        child = self.get_child(request.data.get("username", None))
        event.participants.add(child)
        return Response(event_serializer.data, status=status.HTTP_200_OK)


class DeleteChildToEventAPIView(AddChildToEventAPIView):

    def post(self, request, event_id):
        event = self.get_event(event_id)
        event_serializer = EventPolymorphicSerializer(event)
        child = self.get_child(request.data.get("username", None))
        event.participants.remove(child)
        return Response(event_serializer.data, status=status.HTTP_200_OK)


class SeasonViewSet(viewsets.ModelViewSet):
    queryset = Season.objects.all()
    serializer_class = SeasonSerializer
