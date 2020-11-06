from django.utils import timezone

from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.generics import get_object_or_404

from rest_polymorphic.serializers import PolymorphicSerializer

from core import choices

from apps.events.models import (Event, SkiTraining, SkiRace, Season, Category, Location, RaceOrganizer, EventType,
                                SkisType)
from apps.family.models import Child
from apps.users.models import Profile

from apps.users.api.serializers import BaseProfileSerializer


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


class LocationSerializer(serializers.ModelSerializer):
    displayName = serializers.CharField(source='display_name', read_only=True)

    class Meta:
        model = Location
        fields = "__all__"


class ParticipantsSerializer(serializers.ModelSerializer):
    displayName = serializers.CharField(source='user.full_name', read_only=True)

    class Meta:
        model = Profile
        fields = ("id", "displayName")


class BaseEventSerializer(serializers.ModelSerializer):
    participants = ParticipantsSerializer(many=True, read_only=True)

    def create(self, validated_data):
        validated_data["season"], created = Season.objects.get_or_create(current=True)
        if created:
            print("Season created")
        return super(BaseEventSerializer, self).create(validated_data)

    def to_representation(self, instance):
        # self.fields["accommodation"] = AccommodationSerializer(many=True, read_only=True)
        self.fields["category"] = CategorySerializer(many=True, read_only=True)
        self.fields["skis_type"] = SkisTypeSerializer(many=True, read_only=True)
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


class ProfileStatSerializer(serializers.ModelSerializer):

    def to_representation(self, instance):
        return self.get_data(instance)

    def get_data(self, instance):
        user = instance["user"]
        seasons = instance["seasons"]

        # TODO
        #  Check if is kid
        kid = Child.objects.get(user__profile=user)
        ret = {
            "user": BaseProfileSerializer(instance=user).data,
            "data": {}
        }
        for season in seasons:
            try:
                # TODO category -> user which can be on this event
                # FIXME if event category is none then it breaks
                kid_asc = kid.categories.get(season=season)
                ret["data"][str(season)] = {}
                print("foud and creating child", season)
            except Exception:
                continue
                pass

            for event_type, value in choices.EventTypeChoices.choices:
                # RES: https://docs.djangoproject.com/en/dev/topics/db/queries/#complex-lookups-with-q-objects
                query = {
                    "season"  : season,
                    "type"    : event_type,
                    "end__lte": timezone.now(),
                    "category": kid_asc,
                    "canceled": False
                }

                events = Event.objects.filter(**query).order_by('start')
                ret["data"][str(season)][event_type] = {}
                ret["data"][str(season)][event_type]["name"] = value
                ret["data"][str(season)][event_type]["count"] = user.events.filter(**query).count()
                ret["data"][str(season)][event_type]["total"] = events.count()

        return ret

    class Meta:
        model = Profile
        fields = "__all__"
        read_only_fields = ('user_role',)
