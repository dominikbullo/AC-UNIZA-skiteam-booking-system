from django.contrib import admin

from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Permission

from family.models import FamilyMember
from users.forms import CustomUserCreationForm, CustomUserChangeForm
from users.models import User, Profile


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


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = User
    list_display = UserAdmin.list_display + ("get_identity", "user_role")

    inlines = [ProfileInline, FamilyMemberInLine]

    def get_identity(self, instance):
        try:
            return instance.email_or_username
        except Exception:
            return "Unidentified"

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields' : ("username", "email", "first_name", "last_name", "user_role", "password1", "password2",),
        }),
    )


admin.site.register(User, CustomUserAdmin)
admin.site.register(Profile)
admin.site.register(Permission)
