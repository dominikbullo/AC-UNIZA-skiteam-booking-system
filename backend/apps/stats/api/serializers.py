from apps.events.api.serializers import SeasonSerializer
from apps.events.models import Event, EventType, Season
from apps.family.models import Child
from apps.stats.models import (EventStatistic, PerformanceTestStatistic,
                               RaceStatistic)
from apps.users.api.serializers import BaseProfileSerializer
from apps.users.models import Profile
from django.utils import timezone
from rest_framework import serializers
from rest_polymorphic.serializers import PolymorphicSerializer


class EventStatisticSerializer(serializers.ModelSerializer):
    class Meta:
        fields = "__all__"
        model = EventStatistic


class PerformanceTestStatisticSerializer(serializers.ModelSerializer):
    class Meta:
        fields = "__all__"
        model = PerformanceTestStatistic


class RaceStatisticSerializer(serializers.ModelSerializer):
    class Meta:
        fields = "__all__"
        model = RaceStatistic


class StatisticPolymorphicSerializer(PolymorphicSerializer):
    model_serializer_mapping = {
        EventStatistic: EventStatisticSerializer,
        PerformanceTestStatistic: PerformanceTestStatisticSerializer,
        RaceStatistic: RaceStatisticSerializer,
    }


class ProfileStatSerializer(BaseProfileSerializer):
    """
    Should be for every profile. Now it's just for children. For that i passing children as context to serializer.
    But in feature for every role i could call separate stat serializer.
    e.g:
     Child -> Stat count
     Parent -> Helping count
     Coach -> Number of event (for payment)
    """

    event_stats = serializers.SerializerMethodField()

    def get_event_stats(self, instance):
        if Child.objects.filter(user__profile=instance).exists():
            child = Child.objects.get(user__profile=instance)
            return ChildStatSerializer(
                instance=child, context={"profile": instance}
            ).data

        return

    class Meta:
        model = Profile
        fields = "__all__"


class ChildStatSerializer(serializers.ModelSerializer):
    def to_representation(self, instance):
        return self.get_event_stats(instance)

    def get_event_stats(self, instance):
        ret = {}
        print("categories", instance.categories.all())

        # TODO: filter season by query
        interested_in_categories = instance.categories.all()
        for item in interested_in_categories:
            print("item", item)
            print("item.season", item.season)
            tmp = []

            for event_type in EventType.objects.all():
                # "start__lte" because end could be blank or null
                # TODO: maybe some think that end could not be blank tho
                query = {
                    "category": item,
                    "type": event_type,
                    "start__lte": timezone.now(),
                    "canceled": False,
                }
                events = Event.objects.filter(**query).order_by("start")

                tmp.append(
                    {
                        "type": EventTypeStatSerializer(instance=event_type).data,
                        "count": self.context.get("profile")
                        .events.filter(**query)
                        .count(),
                        "total": events.count(),
                    }
                )

            ret.update({str(item.season): tmp})
        return ret

    class Meta:
        model = Child
        fields = "__all__"


class EventTypeStatSerializer(serializers.ModelSerializer):
    displayName = serializers.CharField(source="display_name", read_only=True)

    class Meta:
        model = EventType
        fields = "__all__"
