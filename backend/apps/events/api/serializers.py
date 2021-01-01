from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.generics import get_object_or_404

from rest_polymorphic.serializers import PolymorphicSerializer

from core import choices

from apps.events.models import (Event, SkiTraining, SkiRace, Season, Category, Location, RaceOrganizer, EventType,
                                SkisType, Accommodation, EventResponse)
from apps.family.models import Child
from apps.users.models import Profile

from apps.users.api.serializers import BaseProfileSerializer, BaseUserSerializer


class SeasonSerializer(serializers.ModelSerializer):
    displayName = serializers.CharField(source='get_name_display', read_only=True)

    class Meta:
        model = Season
        fields = "__all__"


class CategorySerializer(serializers.ModelSerializer):
    displayName = serializers.CharField(source='get_name_display', read_only=True)

    class Meta:
        model = Category
        exclude = ("members",)


# RES: https://github.com/richardtallent/vue-simple-calendar#calendar-item-properties
# RES(Nested relationships): https://medium.com/@raaj.akshar/creating-reverse-related-objects-with-django-rest-framework-b1952ddff1c

class RaceOrganizerSerializer(serializers.ModelSerializer):
    displayName = serializers.CharField(source='display_name', read_only=True)

    class Meta:
        model = RaceOrganizer
        fields = "__all__"


class SkisTypeSerializer(serializers.ModelSerializer):
    displayName = serializers.CharField(source='display_name', read_only=True)

    class Meta:
        model = SkisType
        fields = "__all__"


class EventTypeSerializer(serializers.ModelSerializer):
    displayName = serializers.CharField(source='display_name', read_only=True)

    class Meta:
        model = EventType
        fields = "__all__"


class AccommodationSerializer(serializers.ModelSerializer):
    displayName = serializers.CharField(source='display_name', read_only=True)

    class Meta:
        model = Accommodation
        fields = "__all__"


class LocationSerializer(serializers.ModelSerializer):
    displayName = serializers.CharField(source='display_name', read_only=True)

    class Meta:
        model = Location
        fields = "__all__"


class ParticipantsSerializer(serializers.ModelSerializer):
    displayName = serializers.CharField(source='user.full_name', read_only=True)

    class Meta:
        model = Profile
        fields = ("id", "displayName",)


class EventResponseSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        # for x in validated_data:;
        #     print(f"{x} -> {validated_data[x]}")
        response, created = EventResponse.objects.update_or_create(
            user_to_event=validated_data.get('user_to_event', None),
            event=validated_data.get('event', None))

        response.going = validated_data.get('going', None)
        response.save()
        return response

    def to_representation(self, instance):
        self.fields["user_to_event"] = ParticipantsSerializer(read_only=True)
        to_representation = super(EventResponseSerializer, self).to_representation(instance)
        return to_representation

    class Meta:
        model = EventResponse
        exclude = ("id", "event")


class BaseEventSerializer(serializers.ModelSerializer):
    responses = serializers.SerializerMethodField()

    def get_responses(self, item):
        # get unique newest instance for each child child
        qs = EventResponse.objects.order_by("user_to_event__user_id", "-created_at") \
            .filter(event=item).distinct("user_to_event__user_id")
        serializer = EventResponseSerializer(instance=qs, many=True)
        return serializer.data

    def create(self, validated_data):
        validated_data["season"], created = Season.objects.get_or_create(current=True)
        if created:
            print("Season created_at")
        return super(BaseEventSerializer, self).create(validated_data)

    def to_representation(self, instance):
        # TODO: order category by year from
        # TODO: order location by recent used, or used count
        self.fields["accommodation"] = AccommodationSerializer(many=True, read_only=True)
        self.fields["participants"] = ParticipantsSerializer(many=True, read_only=True)
        self.fields["category"] = CategorySerializer(many=True, read_only=True)
        self.fields["skis_type"] = SkisTypeSerializer(many=True, read_only=True)
        self.fields["location"] = LocationSerializer(instance.location, many=False, read_only=True)
        self.fields["type"] = EventTypeSerializer(instance.type, many=False, read_only=True)

        to_representation = super(BaseEventSerializer, self).to_representation(instance)
        return to_representation

    class Meta:
        fields = "__all__"
        read_only_fields = ("season",)
        # exclude = ("season", "location", "category", "participants")


class EventSerializer(BaseEventSerializer):
    # type = EventTypeSerializer(queryset=EventType.objects.all())

    # def validate(self, data):
    #     validated_data = super(EventSerializer, self).validate(data)
    #     event_type = data.get("type")
    #
    #     # if event_type == get_object_or_404(EventType, type=EventTypeChoices.TRAINING, need_skis=True):
    #     #     raise ValidationError("Bad resourcetype for %s" % event_type)
    #     #
    #     # if event_type == get_object_or_404(EventType, type=EventTypeChoices.RACE, need_skis=True):
    #     #     raise ValidationError("Bad resourcetype for %s" % event_type)
    #
    #     return validated_data

    class Meta(BaseEventSerializer.Meta):
        model = Event


class SkiTrainingSerializer(BaseEventSerializer):
    type = EventTypeSerializer(read_only=True)

    # def validate(self, data):
    #     if event_type != get_object_or_404(EventType, type=EventTypeChoices.TRAINING, need_skis=True):
    #         raise ValidationError("Bad resourcetype for %s" % event_type)
    #     return validated_data

    class Meta(BaseEventSerializer.Meta):
        model = SkiTraining


class SkiRaceSerializer(BaseEventSerializer):
    type = EventTypeSerializer(read_only=True)

    def to_representation(self, instance):
        self.fields["organizer"] = RaceOrganizerSerializer(instance.organizer, many=False, read_only=True)
        return super(SkiRaceSerializer, self).to_representation(instance)

    # def validate(self, data):
    #     validated_data = super(SkiRaceSerializer, self).validate(data)
    #     event_type = data.get("type")
    #     if event_type != get_object_or_404(EventType, type=EventTypeChoices.RACE, need_skis=True):
    #         raise ValidationError("Bad resourcetype for %s" % event_type)
    #     return validated_data

    class Meta(BaseEventSerializer.Meta):
        model = SkiRace


# RES: https://pypi.org/project/django-rest-polymorphic/
class EventPolymorphicSerializer(PolymorphicSerializer):
    model_serializer_mapping = {
        Event      : EventSerializer,
        SkiTraining: SkiTrainingSerializer,
        SkiRace    : SkiRaceSerializer,
    }
