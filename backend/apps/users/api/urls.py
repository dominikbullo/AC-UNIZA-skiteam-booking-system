from apps.users.api.views import (AvatarUpdateView, ChangePasswordView,
                                  ProfileViewSet)
from django.urls import include, path
from rest_framework.routers import DefaultRouter

app_name = "users"

router = DefaultRouter()
router.register(r"profiles?", ProfileViewSet, basename="profile")

urlpatterns = [
    path("profile/<int:pk>/avatar/", AvatarUpdateView.as_view(), name="avatar-update"),
    path(
        "profile/password-change/", ChangePasswordView.as_view(), name="password-change"
    ),
]
