from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from users.models import User


class CustomUserAdmin(UserAdmin):
    # add_form =
    # form =
    model = User
    list_display = ["username", "email", "is_staff"]


admin.site.register(User, CustomUserAdmin)
