from rest_framework import serializers
from events.models import SkiTraining, Event
from rest_polymorphic.serializers import PolymorphicSerializer


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = "__all__"


class SkiTrainingSerializer(serializers.ModelSerializer):
    class Meta:
        model = SkiTraining
        fields = "__all__"
        read_only_fields = ('type',)


# RES: https://pypi.org/project/django-rest-polymorphic/
class EventPolymorphicSerializer(PolymorphicSerializer):
    model_serializer_mapping = {
        Event      : EventSerializer,
        SkiTraining: SkiTrainingSerializer,
    }
