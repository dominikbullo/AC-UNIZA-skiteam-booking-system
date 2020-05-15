from django.utils import timezone

from drf_writable_nested.serializers import WritableNestedModelSerializer

from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from rest_polymorphic.serializers import PolymorphicSerializer

from core import choices

from apps.events.models import Event, SkiTraining, SkiRace, Season, Category, Location, RaceOrganizer
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


class LocationSerializer(serializers.ModelSerializer):
    displayName = serializers.CharField(source='display_name', read_only=True)

    class Meta:
        model = Location
        fields = "__all__"


class BaseEventSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        super(BaseEventSerializer, self).__init__(*args, **kwargs)
        if self.context.get("request") and self.context['request'].method == 'GET':
            self.fields['category'] = CategorySerializer(many=True)
            self.fields['location'] = LocationSerializer(many=False)

    title = serializers.CharField(source='get_type_display', read_only=True)
    season = SeasonSerializer(many=False, read_only=True, required=False)

    category = serializers.PrimaryKeyRelatedField(many=True, queryset=Category.objects.all())
    location = serializers.PrimaryKeyRelatedField(many=False, queryset=Location.objects.all())

    participants = BaseProfileSerializer(many=True, required=False)

    def validate(self, data):
        # If doesnt have season then default current season
        if not data.get('season'):
            data["season"] = Season.objects.get(current=True)

        if data.get('category'):
            for category in data.get('category', ""):
                if category.season.id != data["season"].id:
                    raise ValidationError("Category %s isn't from current season" % str(category))

        return data

    def to_representation(self, instance):
        self.fields["category"] = CategorySerializer(instance.category.all(), many=True, read_only=True)
        self.fields["location"] = LocationSerializer(instance.location, many=False, read_only=True)
        to_representation = super(BaseEventSerializer, self).to_representation(instance)
        return to_representation

    class Meta:
        fields = "__all__"
        depth = 2


class EventSerializer(BaseEventSerializer):

    def validate(self, data):
        validated_data = super(EventSerializer, self).validate(data)
        event_type = data.get("type")
        if event_type == choices.EventTypeChoices.SKI_TRAINING:
            raise ValidationError("Bad resourcetype for %s" % event_type)

        if event_type == choices.EventTypeChoices.SKI_RACE:
            raise ValidationError("Bad resourcetype for %s" % event_type)

        return validated_data

    class Meta:
        model = Event
        exclude = ("polymorphic_ctype",)


class SkiTrainingSerializer(BaseEventSerializer):

    def validate(self, data):
        validated_data = super(SkiTrainingSerializer, self).validate(data)
        # event_type = data.get("type")
        # if event_type != choices.EventTypeChoices.SKI_TRAINING:
        #     raise ValidationError("Bad resourcetype for %s" % event_type)
        return validated_data

    class Meta:
        model = SkiTraining
        fields = "__all__"


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

    class Meta:
        model = SkiRace
        fields = "__all__"


# RES: https://pypi.org/project/django-rest-polymorphic/
class EventPolymorphicSerializer(PolymorphicSerializer):
    model_serializer_mapping = {
        Event      : EventSerializer,
        SkiTraining: SkiTrainingSerializer,
        SkiRace    : SkiRaceSerializer,
    }


class UserStatSerializer(serializers.ModelSerializer):

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
