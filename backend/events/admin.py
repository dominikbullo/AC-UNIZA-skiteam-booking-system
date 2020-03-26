from django.contrib import admin
from django.apps import apps
from django.contrib.admin.sites import AlreadyRegistered

from events.models import Category


class CategoryAdmin(admin.ModelAdmin):
    filter_horizontal = ('members',)


admin.site.register(Category, CategoryAdmin)

app_models = apps.get_app_config('events').get_models()
for model in app_models:
    try:
        admin.site.register(model)
    except AlreadyRegistered:
        pass

# TODO: Admin Event in one form
