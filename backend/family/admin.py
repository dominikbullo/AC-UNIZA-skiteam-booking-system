from django.contrib import admin
from django.apps import apps
from django.contrib.admin.sites import AlreadyRegistered

from family.models import Child


class ChildAdmin(admin.ModelAdmin):
    filter_horizontal = ('categories',)


admin.site.register(Child, ChildAdmin)

app_models = apps.get_app_config('family').get_models()
for model in app_models:
    try:
        admin.site.register(model)
    except AlreadyRegistered:
        pass
