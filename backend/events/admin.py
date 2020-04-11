from django.contrib import admin
from django.apps import apps
from django.contrib.admin.sites import AlreadyRegistered
from django.contrib import admin
from polymorphic.admin import PolymorphicParentModelAdmin, PolymorphicChildModelAdmin, PolymorphicChildModelFilter

from events.models import Event, SkiTraining, SkiRace, Category, Location


# RES: https://django-polymorphic.readthedocs.io/en/stable/admin.html
class ModelAChildAdmin(PolymorphicChildModelAdmin):
    """ Base admin class for all child models """
    base_model = Event  # Optional, explicitly set here.

    __fields = ("season", "type", "location")
    # search_fields = ('season__year', 'type', 'location__name')
    list_filter = __fields
    list_display = PolymorphicParentModelAdmin.list_display + __fields


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
    __fields = ("season", "type", "location")
    # search_fields = ('season__year', 'type', 'location__name')
    list_filter = __fields
    list_display = PolymorphicParentModelAdmin.list_display + __fields


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    filter_horizontal = ('members',)
    __fields = ("name", "season")
    list_filter = __fields
    list_display = admin.ModelAdmin.list_display + __fields

    # On model save auto add every child to this category
    def save_model(self, request, obj, form, change):
        # if not obj.created_by:
        #     obj.created_by = request.user
        obj.save()

    class Media:
        js = (
            "//ajax.googleapis.com/ajax/libs/jquery/3.4.1/jquery.min.js",
            "/static/js/admin.js",
        )


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    __fields = ("name", "ski_slope")
    list_filter = __fields
    list_display = admin.ModelAdmin.list_display + __fields


app_models = apps.get_app_config('events').get_models()
for model in app_models:
    try:
        admin.site.register(model)
    except AlreadyRegistered:
        pass
