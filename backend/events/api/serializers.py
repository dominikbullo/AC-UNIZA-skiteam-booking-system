from rest_framework import serializers
from rest_framework.serializers import raise_errors_on_nested_writes
from rest_framework.utils import model_meta

from events.models import Event, SkiTraining, SkiRace, Season, Category
from rest_polymorphic.serializers import PolymorphicSerializer

from family.api.serializers import ChildProfileSerializer


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
    # TODO decision
    # participants = serializers.HyperlinkedRelatedField(many=True, read_only=True, view_name="family:child-detail")
    participants = ChildProfileSerializer(many=True)

    def update(self, instance, validated_data):
        raise_errors_on_nested_writes('update', self, validated_data)
        info = model_meta.get_field_info(instance)

        # Simply set each attribute on the instance, and then save it.
        # Note that unlike `.create()` we don't need to treat many-to-many
        # relationships as being a special case. During updates we already
        # have an instance pk for the relationships to be associated with.
        m2m_fields = []
        for attr, value in validated_data.items():
            if attr in info.relations and info.relations[attr].to_many:
                m2m_fields.append((attr, value))
            else:
                setattr(instance, attr, value)

        instance.save()

        # Note that many-to-many fields are set after updating instance.
        # Setting m2m fields triggers signals which could potentially change
        # updated instance and we do not want it to collide with .update()
        for attr, value in m2m_fields:
            field = getattr(instance, attr)
            field.set(value)

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
