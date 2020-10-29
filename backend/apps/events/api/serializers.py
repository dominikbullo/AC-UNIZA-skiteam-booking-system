from django.utils import timezone

from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from rest_polymorphic.serializers import PolymorphicSerializer

from core import choices

from apps.events.models import Event, SkiTraining, SkiRace, Season, Category, Location, RaceOrganizer, EventType
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
        fields = ("displayName",)


class EventTypeSerializer(serializers.ModelSerializer):
    displayName = serializers.CharField(source='get_name_display', read_only=True)

    class Meta:
        model = EventType
        exclude = ("id",)


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
    # startTime = serializers.CharField(source="start", read_only=True)
    # endTime = serializers.CharField(source="end", read_only=True)
    # startRecur = serializers.CharField(source="start", read_only=True)
    # endRecur = serializers.CharField(source="end", read_only=True)

    type = EventTypeSerializer(read_only=True)
    participants = ParticipantsSerializer(many=True, read_only=True)

    class Meta:
        fields = "__all__"
        # exclude = ("season", "location", "category", "participants")


class EventSerializer(BaseEventSerializer):

    def validate(self, data):
        validated_data = super(EventSerializer, self).validate(data)
        event_type = data.get("type")

        if event_type == choices.EventTypeChoices.SKI_TRAINING:
            raise ValidationError("Bad resourcetype for %s" % event_type)

        if event_type == choices.EventTypeChoices.SKI_RACE:
            raise ValidationError("Bad resourcetype for %s" % event_type)

        return validated_data

    class Meta(BaseEventSerializer.Meta):
        model = Event


class SkiTrainingSerializer(BaseEventSerializer):
    # def validate(self, data):
    #     # query = {
    #     #     "name"     : EventTypeChoices.TRAINING,
    #     #     "need_skis": True
    #     # }
    #     validated_data = super(SkiTrainingSerializer, self).validate(data)
    #     # event_type = data.get("type")
    #     # event_type = EventType.objects.exists(**query).first()
    #     # if event_type != EventType.objects.exists(**query).first()
    #     #     raise ValidationError("Bad resourcetype for %s" % event_type)
    #     return validated_data

    class Meta(BaseEventSerializer.Meta):
        model = SkiTraining


class SkiRaceSerializer(BaseEventSerializer):
    def __init__(self, *args, **kwargs):
        super(SkiRaceSerializer, self).__init__(*args, **kwargs)
        if self.context.get("request") and self.context['request'].method == 'GET':
            self.fields['organizer'] = RaceOrganizerSerializer(many=True)

    organizer = serializers.PrimaryKeyRelatedField(many=False, queryset=RaceOrganizer.objects.all())

    def validate(self, data):
        validated_data = super(SkiRaceSerializer, self).validate(data)
        event_type = data.get("type")
        if event_type != choices.EventTypeChoices.SKI_RACE:
            raise ValidationError("Bad resourcetype for %s" % event_type)
        return validated_data

    def to_representation(self, instance):
        self.fields["organizer"] = RaceOrganizerSerializer(instance.organizer, many=False, read_only=True)
        to_representation = super(SkiRaceSerializer, self).to_representation(instance)
        return to_representation

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
