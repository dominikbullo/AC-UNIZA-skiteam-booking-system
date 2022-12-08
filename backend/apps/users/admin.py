from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Permission

from apps.family.models import FamilyMember
from apps.users.forms import CustomUserChangeForm, CustomUserCreationForm
from apps.users.models import Profile, User


class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = "Profile"
    fk_name = "user"
    filter_horizontal = ("events",)


# class ChildInline(admin.StackedInline):
#     model = Child
#     can_delete = False
#     verbose_name_plural = 'Children'
#     fk_name = 'user'


class FamilyMemberInLine(admin.StackedInline):
    model = FamilyMember
    can_delete = False
    verbose_name_plural = "Families"
    fk_name = "user"


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = User
    list_display = UserAdmin.list_display + (
        "date_joined",
        "last_login",
        "get_user_role",
    )

    inlines = [ProfileInline, FamilyMemberInLine]

    def get_user_role(self, instance):
        try:
            return instance.profile.user_role
        except Exception:
            return "Unidentified"

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "username",
                    "email",
                    "first_name",
                    "last_name",
                    "password1",
                    "password2",
                ),
            },
        ),
    )


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    filter_horizontal = ("events",)


admin.site.register(Permission)
