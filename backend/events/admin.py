from django.contrib import admin
from django.apps import apps
from django.contrib.admin.sites import AlreadyRegistered
from django.contrib import admin
from polymorphic.admin import PolymorphicParentModelAdmin, PolymorphicChildModelAdmin, PolymorphicChildModelFilter

from events.models import Event, SkiTraining, SkiRace, Category


# RES: https://django-polymorphic.readthedocs.io/en/stable/admin.html
class ModelAChildAdmin(PolymorphicChildModelAdmin):
    """ Base admin class for all child models """
    base_model = Event  # Optional, explicitly set here.


@admin.register(SkiTraining)
class SkiRaceAdmin(ModelAChildAdmin):
    base_model = SkiTraining  # Explicitly set here!
    show_in_index = True  # makes child model admin visible in main admin site

    # define custom features here


@admin.register(SkiRace)
class SkiTrainingAdmin(ModelAChildAdmin):
    base_model = SkiRace  # Explicitly set here!
    show_in_index = True  # makes child model admin visible in main admin site
    # define custom features here


@admin.register(Event)
class ModelAParentAdmin(PolymorphicParentModelAdmin):
    """ The parent model admin """
    base_model = Event  # Optional, explicitly set here.
    child_models = (Event, SkiTraining, SkiRace)
    list_filter = (PolymorphicChildModelFilter,)  # This is optional.


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    filter_horizontal = ('members',)


app_models = apps.get_app_config('events').get_models()
for model in app_models:
    try:
        admin.site.register(model)
    except AlreadyRegistered:
        pass
