from rest_framework import serializers

from app.settings.dev import CALENDAR_DATETIME_FORMAT
from events.models import Event, SkiTraining, SkiRace, Season
from rest_polymorphic.serializers import PolymorphicSerializer


class SeasonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Season
        fields = "__all__"


# id - A unique identifier for the item. This is required and must be unique.

# startDate - The date the item starts on the calendar. This must be either passed as a JavaScript date object,
# or as a string following an ISO-like form of "yyyy-mm-dd HH:MM:SS" (time is optional, and within time,
# minutes and seconds are both optional).

# endDate - The date the item ends on the calendar. Defaults to the same date as startDate. This must be either
# passed as a JavaScript date object, or as a string following an ISO-like form of "yyyy-mm-dd HH:MM:SS"
# (time is optional, and within time, minutes and seconds are both optional).

# title - The name of the item shown on the calendar. Defaults to "Untitled".

# url - The URL associated with the item. The component has no built-in action associated with this,
# but it does add a "hasUrl" class to the item. To "follow" the URL, you'll need to listen for the click-event
# event and take the appropriate action.

# classes - A String with any additional CSS classes you wish to assign to the item.
# style - A String with any additional CSS styles you wish to apply to the item.

# RES: https://github.com/richardtallent/vue-simple-calendar#calendar-item-properties
class BaseEventSerializer(serializers.ModelSerializer):
    startDate = serializers.DateTimeField(source='start_date', read_only=True)
    endDate = serializers.DateTimeField(source='end_date', read_only=True)
    start = serializers.DateTimeField(source='start_date', read_only=True)
    end = serializers.DateTimeField(source='end_date', read_only=True)
    title = serializers.CharField(source='type', read_only=True)
    participants = serializers.HyperlinkedRelatedField(many=True, read_only=True, view_name="family:child-detail")


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
