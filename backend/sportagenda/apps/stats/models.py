from django.db import models
from polymorphic.models import PolymorphicModel
from sportagenda.apps.events.models import Season
from sportagenda.apps.users.models import Profile, User


class Statistic(PolymorphicModel):
    season = models.ForeignKey(Season, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class EventStatistic(Statistic):
    add = models.IntegerField(blank=True, null=True, default=0)
    subtract = models.IntegerField(blank=True, null=True, default=0)
    total_add = models.IntegerField(blank=True, null=True, default=0)
    total_subtract = models.IntegerField(blank=True, null=True, default=0)


class PerformanceTestStatistic(Statistic):
    date = models.DateField()
    long_jump = models.FloatField(blank=True, null=True, default=0)
    high_jump = models.FloatField(blank=True, null=True, default=0)
    twelve_minutes_run = models.DurationField(
        blank=True, null=True, default="00:00", help_text='"MM:SS" format'
    )
    boating = models.DurationField(
        blank=True, null=True, default="00:00", help_text='"MM:SS" format'
    )


class RaceStatistic(Statistic):
    date = models.DateField()
    position = models.IntegerField(blank=True, null=True, default=0)
    diff_to_first = models.FloatField(blank=True, null=True, default=0)
