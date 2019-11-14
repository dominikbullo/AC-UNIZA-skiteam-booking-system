from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Permission

from users.models import User, Profile, ProfileStatus


class CustomUserAdmin(UserAdmin):
    # add_form =
    # form =
    model = User
    list_display = ["username", "email", "is_staff"]


admin.site.register(User, CustomUserAdmin)
admin.site.register(Permission)

admin.site.register(Profile)
admin.site.register(ProfileStatus)
