from django.utils import timezone
from rest_framework import serializers

from rest_polymorphic.serializers import PolymorphicSerializer

from apps.family.api.serializers import ChildSerializer
from core import choices
from apps.events.models import Event, SkiTraining, SkiRace, Season, Category

from apps.family.models import Child
from apps.users.api.serializers import BaseProfileSerializer
from apps.users.models import Profile


class SeasonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Season
        fields = "__all__"


class CategorySerializer(serializers.ModelSerializer):
    displayName = serializers.CharField(source='get_name_display', read_only=True)
    season = SeasonSerializer(many=False, read_only=True)

    # TODO LESS info base user serializer? Idk
    # members = ChildSerializer(many=True)

    class Meta:
        model = Category
        fields = "__all__"


# RES: https://github.com/richardtallent/vue-simple-calendar#calendar-item-properties
# RES(Nested relationships): https://medium.com/@raaj.akshar/creating-reverse-related-objects-with-django-rest-framework-b1952ddff1c
class BaseEventSerializer(serializers.ModelSerializer):
    title = serializers.CharField(source='get_type_display', read_only=True)

    # RES: http://www.tomchristie.com/rest-framework-2-docs/api-guide/relations
    participants = BaseProfileSerializer(many=True, required=False)
    season = SeasonSerializer(many=False, read_only=True)
    category = CategorySerializer(many=True, read_only=True)

    def validate(self, data):
        # don't want to change any type
        participants = data.get('participants', None)

        # If doesnt have season then default current season
        if not data.get('season', None):
            data["season"] = Season.objects.get(current=True)

        # TODO: If all categories are from same season
        return data

    #  RES(update): https://riptutorial.com/django-rest-framework/example/25521/updatable-nested-serializers
    #  RES(delete): https://stackoverflow.com/questions/42159480/delete-member-of-many-to-many-relationship-django-rest-framework
    #  RES: https://stackoverflow.com/questions/28706072/drf-3-creating-many-to-many-update-create-serializer-with-though-table
    def update(self, instance, validated_data):
        participants = validated_data.get('participants', None)

        instance = super(BaseEventSerializer, self).update(instance, validated_data)
        instance.save()
        return instance

class EventSerializer(BaseEventSerializer):
    class Meta:
        model = Event
        fields = "__all__"


class SkiTrainingSerializer(BaseEventSerializer):
    class Meta:
        model = SkiTraining
        fields = "__all__"
        read_only_fields = ('type',)


class SkiRaceSerializer(BaseEventSerializer):
    class Meta:
        model = SkiRace
        fields = "__all__"
        read_only_fields = ('type',)


# RES: https://pypi.org/project/django-rest-polymorphic/
class EventPolymorphicSerializer(PolymorphicSerializer):
    model_serializer_mapping = {
        Event      : EventSerializer,
        SkiTraining: SkiTrainingSerializer,
        SkiRace    : SkiRaceSerializer,
    }

    # RES: https://stackoverflow.com/a/51905746/10523982
    def to_resource_type(self, model_or_instance):
        return model_or_instance._meta.object_name.lower()


class UserStatSerializer(serializers.ModelSerializer):

    def to_representation(self, instance):
        return self.get_data(instance)

    def get_data(self, instance):
        user = instance["user"]
        seasons = instance["seasons"]

        # TODO
        #  Check if is kid
        kid = Child.objects.get(user__profile=user)
        ret = {}
        for season in seasons:
            print("season ", season)
            try:
                # TODO category -> user which can be on this event
                kid_asc = kid.categories.get(season=season)
                ret[str(season)] = {}
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
                ret[str(season)][event_type] = {}
                ret[str(season)][event_type]["name"] = value
                ret[str(season)][event_type]["count"] = user.events.filter(**query).count()
                ret[str(season)][event_type]["total"] = events.count()

        return ret

    class Meta:
        model = Profile
        fields = "__all__"
        read_only_fields = ('user_role',)
