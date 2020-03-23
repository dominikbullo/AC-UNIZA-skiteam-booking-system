from django.contrib import admin

from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Permission

from family.models import FamilyMember
from users.forms import CustomUserCreationForm, CustomUserChangeForm
from users.models import User, Profile

from core.choices import USER_TYPE_CHOICES


class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Profile'
    fk_name = 'user'


class FamilyMemberInLine(admin.StackedInline):
    model = FamilyMember
    can_delete = False
    verbose_name_plural = 'Families'
    fk_name = 'user'


# https: // simpleisbetterthancomplex.com / tutorial / 2016 / 07 / 22 / how - to - extend - django - user - model.html


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = User
    list_display = ["get_identity", "first_name", "last_name", "date_joined", "last_login", "get_type", "is_staff"]
    inlines = [ProfileInline, FamilyMemberInLine]

    def get_type(self, instance):
        try:
            return dict(USER_TYPE_CHOICES)[instance.profile.user_type]
        except Exception:
            return "Unidentified"

    def get_identity(self, instance):
        try:
            return instance.email_or_username
        except Exception:
            return "Unidentified"

    get_type.short_description = 'User type'

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields' : ("username", "email", "first_name", "last_name", "password1", "password2",),
        }),
    )


admin.site.register(User, CustomUserAdmin)
admin.site.register(Profile)
admin.site.register(Permission)
