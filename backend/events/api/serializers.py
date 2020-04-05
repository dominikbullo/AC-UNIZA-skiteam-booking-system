from django.utils import timezone
from rest_framework import serializers

from core import choices
from events.models import Event, SkiTraining, SkiRace, Season
from rest_polymorphic.serializers import PolymorphicSerializer

from family.models import Child
from users.api.serializers import BaseProfileSerializer
from users.models import Profile


class SeasonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Season
        fields = "__all__"


# RES: https://github.com/richardtallent/vue-simple-calendar#calendar-item-properties
# RES(Nested relationships): https://medium.com/@raaj.akshar/creating-reverse-related-objects-with-django-rest-framework-b1952ddff1c
class BaseEventSerializer(serializers.ModelSerializer):
    start = serializers.DateTimeField(source='start_date', read_only=True)
    end = serializers.DateTimeField(source='end_date', read_only=True)
    title = serializers.CharField(source='type', read_only=True)

    # RES: http://www.tomchristie.com/rest-framework-2-docs/api-guide/relations
    participants = BaseProfileSerializer(many=True)

    #  RES(update): https://riptutorial.com/django-rest-framework/example/25521/updatable-nested-serializers
    #  RES(delete): https://stackoverflow.com/questions/42159480/delete-member-of-many-to-many-relationship-django-rest-framework
    #  RES: https://stackoverflow.com/questions/28706072/drf-3-creating-many-to-many-update-create-serializer-with-though-table
    def update(self, instance, validated_data):
        # TODO if updating then -> set all? Probably yes
        # FIXME
        participants = validated_data.pop('participants')
        print(*participants, sep=", ")
        instance = super(BaseEventSerializer, self).update(instance, validated_data)
        instance.participants.set(participants)
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
                ret[season.__str__()] = {}
                print("foud and creating child", season)
            except Exception:
                continue
                pass

            for key in choices.EventTypeChoices:
                # If category was in current season event must be in current season too //fail safe
                print("Test", kid_asc)
                # RES: https://docs.djangoproject.com/en/dev/topics/db/queries/#complex-lookups-with-q-objects
                query = {
                    "season"       : season,
                    "type"         : key,
                    "end_date__lte": timezone.now(),
                    "category"     : kid_asc,
                    "canceled"     : False
                }

                event = Event.objects.filter(**query).order_by('start_date').count()

                ret[str(season)][key] = user.events.filter(**query).count()
                ret[str(season)][key + "_total"] = event

        return ret

    class Meta:
        model = Profile
        fields = "__all__"
        read_only_fields = ('user_role',)
