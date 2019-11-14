from django.contrib import admin

from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Permission

from users.forms import CustomUserCreationForm, CustomUserChangeForm
from users.models import User, Profile

from core.utils import USER_TYPE_CHOICES


class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Profile'
    fk_name = 'user'


# https: // simpleisbetterthancomplex.com / tutorial / 2016 / 07 / 22 / how - to - extend - django - user - model.html


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = User
    list_display = ["email", "username", "first_name", "last_name", "get_type"]
    inlines = [ProfileInline]

    def get_type(self, instance):
        return dict(USER_TYPE_CHOICES)[instance.profile.user_type]

    get_type.short_description = 'User type'


# admin.site.unregister(auth.models.User)
admin.site.register(User, CustomUserAdmin)
admin.site.register(Profile)
admin.site.register(Permission)
