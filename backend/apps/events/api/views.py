from django.http import Http404
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.events.models import Event, Season, Category
from apps.events.api.serializers import (EventPolymorphicSerializer, SeasonSerializer, CategorySerializer,
                                         EventChangePolymorphicSerializer)
from apps.events.api.permissions import IsOwnerOrReadOnly, IsOwnFamilyOrReadOnly

# RES: https://github.com/LondonAppDeveloper/recipe-app-api/blob/master/app/recipe/views.py
# RES: https://stackoverflow.com/questions/51016896/how-to-serialize-inherited-models-in-django-rest-framework
from apps.users.models import Profile
from core.choices import get_all_choices
from core.views import get_custom_queryset


class CategoryViewSet(viewsets.ModelViewSet):
    serializer_class = CategorySerializer

    def get_queryset(self):
        return get_custom_queryset(self.request, Category).order_by('year_from')


class EventViewSet(viewsets.ModelViewSet):
    serializer_class = EventPolymorphicSerializer

    # permission_classes = [IsOwnFamilyOrReadOnly]
    # filter_backends = [SearchFilter]
    # search_fields = ["name"]

    # https://github.com/LondonAppDeveloper/recipe-app-api/blob/master/app/recipe/views.py
    def get_serializer_class(self):
        """Return appropriate serializer class"""
        custom = ["create", "update", "partial_update"]
        if self.action in custom:
            return EventChangePolymorphicSerializer
        return EventPolymorphicSerializer

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

        users = request.data.get("users", None)
        if not users:
            Response(status=status.HTTP_400_BAD_REQUEST)

        failed = []
        for user in users.get("add", ""):
            # print("add", user)
            try:
                event.participants.add(self.get_user_profile(user))
            except Http404:
                failed.append(user)
                print("User", user, "not found")
                # raise ValidationError("User %s not found" % user)
                pass

        for user in users.get("delete", ""):
            # print("delete", user)
            try:
                event.participants.remove(self.get_user_profile(user))
            except Http404:
                failed.append(user)
                print("User", user, "not found")
                # raise ValidationError("User %s not found" % user)
                pass

        if len(failed) > 0:
            return Response({"failed": failed}, status=status.HTTP_404_NOT_FOUND)

        return Response(event_serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, url_path='choices')
    def get_event_choices(self, request):
        return Response(get_all_choices(), status=status.HTTP_200_OK)

    def get_queryset(self):
        return get_custom_queryset(self.request, Event).order_by('start')


class SeasonViewSet(viewsets.ModelViewSet):
    queryset = Season.objects.all()
    serializer_class = SeasonSerializer
