from django.db import transaction
from django.http import Http404
from django.shortcuts import get_object_or_404
from django_filters import rest_framework as filters
from rest_framework import viewsets, status, generics, mixins
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from apps.events.models import (Event, Season, Category, Location, RaceOrganizer, EventType, SkisType, Accommodation,
                                EventResponse)
from apps.events.api.serializers import (EventPolymorphicSerializer, SeasonSerializer, CategorySerializer,
                                         LocationSerializer, RaceOrganizerSerializer, EventTypeSerializer,
                                         SkisTypeSerializer, AccommodationSerializer, EventResponseSerializer)

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
        return get_object_custom_queryset(self.request, Category)


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


# RES: https://stackoverflow.com/a/61490489/10523982
class EventResponseCreateAPIView(generics.CreateAPIView):
    queryset = EventResponse.objects.all().order_by('created_at')
    serializer_class = EventResponseSerializer

    # filter_backends = (filters.DjangoFilterBackend,)
    # filterset_fields = ('event', "answerer", "user_to_event",)

    def perform_create(self, serializer):
        answerer = self.request.user.profile

        kwarg_pk = self.kwargs.get("pk")
        event = get_object_or_404(Event, id=kwarg_pk)

        going = self.request.data.get("going", None)
        user_to_event = self.request.data.get("user_to_event", None)

        # Do not create response if you already have same answer as newest entry in DB
        # FIXME : do not check only responses but also participants on event -> maybe thats event better solution
        # if event.responses.filter(user_to_event=user_to_event).exists() and \
        #         event.responses.filter(user_to_event=user_to_event).order_by("-created_at").first().going == going:
        #     raise ValidationError("User is already up to date with your answer")

        # Save the response first (in case of failure)
        self.manage_user_on_event(get_object_or_404(Profile, id=user_to_event), event, going)
        serializer.save(event=event)

    def manage_user_on_event(self, profile, event, going):
        req_user_family_id = self.request.user.familymember.family_id
        # print("user_family_id", user_family_id)

        add_to_event_user_family_id = profile.user.familymember.family_id
        # print("user_family_id", user_to_add_family_id)

        if req_user_family_id != add_to_event_user_family_id:
            # TODO: create some log about this error
            raise ValidationError("You cannot add user from another family to event")

        if going:
            event.participants.add(profile)
        else:
            event.participants.remove(profile)
