from rest_framework import serializers

from events.models import Event, SkiTraining, SkiRace, Season
from rest_polymorphic.serializers import PolymorphicSerializer

from users.api.serializers import BaseProfileSerializer


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

    # TODO FIXME: update via rest
    # participants = serializers.HyperlinkedRelatedField(many=True, read_only=True, view_name='users:user-detail')

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
    # def create(self, validated_data):
    #     resource_type = validated_data.pop(self.resource_type_field_name)
    #     serializer = self._get_serializer_from_resource_type(resource_type)
    #     return serializer.create(validated_data)
    #
    # def update(self, instance, validated_data):
    #     resource_type = validated_data.pop(self.resource_type_field_name)
    #     serializer = self._get_serializer_from_resource_type(resource_type)
    #     return serializer.update(instance, validated_data)

    model_serializer_mapping = {
        Event      : EventSerializer,
        SkiTraining: SkiTrainingSerializer,
        SkiRace    : SkiRaceSerializer,
    }

    # RES: https://stackoverflow.com/a/51905746/10523982
    def to_resource_type(self, model_or_instance):
        return model_or_instance._meta.object_name.lower()
