from django.http import Http404
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView

from events.models import Event, Season
from events.api.serializers import EventPolymorphicSerializer, SeasonSerializer
from events.api.permissions import IsOwnerOrReadOnly, IsOwnFamilyOrReadOnly

# RES: https://github.com/LondonAppDeveloper/recipe-app-api/blob/master/app/recipe/views.py
# RES: https://stackoverflow.com/questions/51016896/how-to-serialize-inherited-models-in-django-rest-framework
from users.models import Profile


class EventViewSet(viewsets.ModelViewSet):
    serializer_class = EventPolymorphicSerializer

    # permission_classes = [IsOwnFamilyOrReadOnly]
    # filter_backends = [SearchFilter]
    # search_fields = ["name"]

    def get_event(self, pk):
        return get_object_or_404(Event, pk=pk)

    def get_user_profile(self, username):
        return get_object_or_404(Profile, user__username=username)

    # RES: https://stackoverflow.com/questions/36365326/django-rest-framework-doesnt-serialize-serializermethodfield
    @action(detail=True, methods=['post'], url_path='change')
    def add_users_to_event(self, request, pk=None):
        event_id = pk
        event = self.get_event(event_id)
        event_serializer = EventPolymorphicSerializer(event)

        # RELEASE delete this test data
        # request.data["users"]["add"] = ["testsets", "asdasdaasdasd", "asdasdasdasdas", "sdasda"]
        # request.data["users"]["delete"] = []

        users = request.data.get("users", None)
        if not users:
            Response(status=status.HTTP_400_BAD_REQUEST)

        # [] -> delete everyove
        # ["admin"] -> find my child, remove every, add only admin
        # ["admin", "ASdasd", "Asdasd", "asdasd"] -> find my child, remove every, add only admin
        failed = []
        for user in users.get("add", ""):
            # print("add", user)
            try:
                event.participants.add(self.get_user_profile(user))
            except Http404:
                failed.append(user)
                print("User", user, "not found")
                pass

        for user in users.get("delete", ""):
            # print("delete", user)
            try:
                event.participants.remove(self.get_user_profile(user))
            except Http404:
                failed.append(user)
                print("User", user, "not found")
                pass

        if len(failed) > 0:
            return Response(failed, status=status.HTTP_404_NOT_FOUND)

        return Response(event_serializer.data, status=status.HTTP_200_OK)

    def get_queryset(self):
        queryset = Event.objects.all()

        if self.request.query_params.get('season') == "current":
            print("Getting events from current season")
            queryset = queryset.filter(season=Season.objects.get(current=True))

        return queryset


class SeasonViewSet(viewsets.ModelViewSet):
    queryset = Season.objects.all()
    serializer_class = SeasonSerializer
