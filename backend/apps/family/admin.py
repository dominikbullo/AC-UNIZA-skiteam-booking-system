from apps.family.models import Family, FamilyMember
from django.apps import apps
from django.contrib import admin
from django.contrib.admin.sites import AlreadyRegistered


class FamilyMemberInLine(admin.StackedInline):
    model = FamilyMember
    verbose_name_plural = "Families"
    fk_name = "family"


@admin.register(Family)
class CustomFamilyAdmin(admin.ModelAdmin):
    inlines = [FamilyMemberInLine]


app_models = apps.get_app_config("family").get_models()
for model in app_models:
    try:
        admin.site.register(model)
    except AlreadyRegistered:
        pass
