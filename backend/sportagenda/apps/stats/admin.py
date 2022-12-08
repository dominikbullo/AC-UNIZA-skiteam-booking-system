from django.apps import apps
from django.contrib import admin
from django.contrib.admin.sites import AlreadyRegistered
from polymorphic.admin import (PolymorphicChildModelAdmin,
                               PolymorphicParentModelAdmin)
from sportagenda.apps.stats.models import (EventStatistic,
                                           PerformanceTestStatistic,
                                           RaceStatistic, Statistic)


# RES: https://django-polymorphic.readthedocs.io/en/stable/admin.html
class StatisticChildAdmin(PolymorphicChildModelAdmin):
    """Base admin class for all child models"""

    base_model = Statistic  # Optional, explicitly set here.


@admin.register(EventStatistic)
class EventStatisticAdmin(StatisticChildAdmin):
    base_model = EventStatistic  # Explicitly set here!


@admin.register(PerformanceTestStatistic)
class PerformanceTestStatisticAdmin(StatisticChildAdmin):
    base_model = PerformanceTestStatistic  # Explicitly set here!


@admin.register(RaceStatistic)
class RaceStatisticAdmin(StatisticChildAdmin):
    base_model = RaceStatistic  # Explicitly set here!


@admin.register(Statistic)
class StatisticAdmin(PolymorphicParentModelAdmin):
    """The parent model admin"""

    base_model = Statistic  # Optional, explicitly set here.
    child_models = (EventStatistic, PerformanceTestStatistic, RaceStatistic)


# Register your models here.
app_models = apps.get_app_config("stats").get_models()
for model in app_models:
    try:
        admin.site.register(model)
    except AlreadyRegistered:
        pass
