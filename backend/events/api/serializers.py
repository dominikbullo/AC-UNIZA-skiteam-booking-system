from rest_framework import serializers
from events.models import Event, SkiTraining, SkiRace, Season
from rest_polymorphic.serializers import PolymorphicSerializer


class SeasonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Season
        fields = "__all__"


class EventSerializer(serializers.ModelSerializer):
    participants = serializers.HyperlinkedRelatedField(many=True, read_only=True, view_name="family:child-detail")

    class Meta:
        model = Event
        fields = "__all__"


class SkiTrainingSerializer(serializers.ModelSerializer):
    participants = serializers.HyperlinkedRelatedField(many=True, read_only=True, view_name="family:child-detail")

    class Meta:
        model = SkiTraining
        fields = "__all__"
        # read_only_fields = ('type',)


class SkiRaceSerializer(serializers.ModelSerializer):
    participants = serializers.HyperlinkedRelatedField(many=True, read_only=True, view_name="family:child-detail")

    class Meta:
        model = SkiRace
        fields = "__all__"
        # read_only_fields = ('type',)


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
