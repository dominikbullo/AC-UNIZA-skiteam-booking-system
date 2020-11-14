from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.http import Http404
from django.shortcuts import get_object_or_404
from django_filters import rest_framework as filters
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from apps.events.models import Event, Season, Category, Location, RaceOrganizer, EventType, SkisType, Accommodation
from apps.events.api.serializers import (EventPolymorphicSerializer, SeasonSerializer, CategorySerializer,
                                         LocationSerializer, RaceOrganizerSerializer, EventTypeSerializer,
                                         SkisTypeSerializer, AccommodationSerializer)

# RES: https://github.com/LondonAppDeveloper/recipe-app-api/blob/master/app/recipe/views.py
# RES: https://stackoverflow.com/questions/51016896/how-to-serialize-inherited-models-in-django-rest-framework
from apps.family.models import Child, FamilyMember
from apps.users.models import Profile
from core.choices import get_all_choices, UserTypeChoices
from core.permissions import IsCoachOrReadOnly
from core.views import get_object_custom_queryset


class CategoryViewSet(viewsets.ModelViewSet):
    serializer_class = CategorySerializer

    def get_queryset(self):
        return get_object_custom_queryset(self.request, Category).order_by('year_from')


class MyFilterBackend(filters.DjangoFilterBackend):
    def get_filterset_kwargs(self, request, queryset, view):
        kwargs = super().get_filterset_kwargs(request, queryset, view)

        # merge filterset kwargs provided by view class
        if hasattr(view, 'get_filterset_kwargs'):
            kwargs.update(view.get_filterset_kwargs())

        return kwargs


# RES: https://django-filter.readthedocs.io/en/stable/guide/rest_framework.html
class EventsFilter(filters.FilterSet):
    def __init__(self, *args, author=None, **kwargs):
        super().__init__(*args, **kwargs)
        # do something w/ author

    class Meta:
        model = Event
        fields = ['start', 'end', 'type', "participants"]


class EventViewSet(viewsets.ModelViewSet):
    serializer_class = EventPolymorphicSerializer
    permission_classes = [IsCoachOrReadOnly]
    filter_backends = (MyFilterBackend,)
    filterset_class = EventsFilter

    def get_event(self, pk):
        return get_object_or_404(Event, pk=pk)

    # RES: https://stackoverflow.com/questions/36365326/django-rest-framework-doesnt-serialize-serializermethodfield
    @action(detail=True, methods=['post'], url_path='change', permission_classes=[IsAuthenticatedOrReadOnly])
    def add_users_to_event(self, request, pk=None):
        participants = request.data.get("participants", None)
        if not participants:
            Response(status=status.HTTP_400_BAD_REQUEST)

        failed = []
        event_id = pk
        event = self.get_event(event_id)
        event_serializer = EventPolymorphicSerializer(event)

        user_family_id = request.user.familymember.family_id
        print(f"Request from family {user_family_id}")

        children = FamilyMember.objects.filter(family__id=user_family_id).values_list('user__profile__id', flat=True)
        print(f"Children from family {user_family_id}: {children}")

        do_not_touch_these = event.participants.exclude(id__in=children)
        print("do_not_touch_these", do_not_touch_these)

        interested_in = event.participants.filter(id__in=children)
        print("interested_in", interested_in)

        event_without_user_children = event.participants.remove(*interested_in)
        print("event_without", event_without_user_children)

        for profile_ID in participants:
            try:
                event.participants.add(get_object_or_404(Profile, id=profile_ID))
            except Http404:
                failed.append(profile_ID)
                print("User with profile id", profile_ID, "not found")
                # raise ValidationError("Profile %s not found" % profile_ID)
                pass

        if len(failed) > 0:
            return Response({"failed": failed}, status=status.HTTP_404_NOT_FOUND)

        return Response(event_serializer.data, status=status.HTTP_200_OK)

    # TODO: view to add/delete accommodation of event
    @action(detail=True, methods=['post'], url_path='accommodation', permission_classes=[IsAuthenticatedOrReadOnly])
    def add_accommodation(self, request, pk=None):
        # raise Exception('Not Implemented yet!')
        print(f"request is{request}")
        print(f"pk is{pk}")
        # event_id = pk
        event = self.get_event(pk)
        event_serializer = EventPolymorphicSerializer(event)
        # get  { "accommodation": [1,2,3] }
        data = request.data.get("accommodation", None)
        if data:
            print(f"data {data}")
            for acc in data:
                print(f"for loop {acc}")
                if Accommodation.objects.filter(id=acc).exists():
                    event.accommodation.add(acc)
                else:
                    raise Exception("Object not exist in DB. You are trying to add non existing Accommodation ")

        return Response(event_serializer.data, status=status.HTTP_200_OK)

    def get_queryset(self):
        return get_object_custom_queryset(self.request, Event).order_by('start')


class SeasonViewSet(viewsets.ModelViewSet):
    queryset = Season.objects.all().order_by("start_date")
    serializer_class = SeasonSerializer


class LocationViewSet(viewsets.ModelViewSet):
    queryset = Location.objects.all().order_by('name')
    serializer_class = LocationSerializer


class RaceOrganizerViewSet(viewsets.ModelViewSet):
    queryset = RaceOrganizer.objects.all().order_by('name')
    serializer_class = RaceOrganizerSerializer


class EventTypeViewSet(viewsets.ModelViewSet):
    queryset = EventType.objects.all()
    serializer_class = EventTypeSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_fields = ('need_skis',)


class SkisTypeViewSet(viewsets.ModelViewSet):
    queryset = SkisType.objects.all()
    serializer_class = SkisTypeSerializer


class AccommodationViewSet(viewsets.ModelViewSet):
    queryset = Accommodation.objects.all()
    serializer_class = AccommodationSerializer
