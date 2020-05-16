from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.users.api.views import ProfileViewSet, AvatarUpdateView, ChangePasswordView

app_name = 'users'

router = DefaultRouter()
router.register(r"profiles?", ProfileViewSet, basename="profile")

urlpatterns = [
    path("profile/<int:pk>/avatar/", AvatarUpdateView.as_view(), name="avatar-update"),
    path("profile/<int:pk>/password-change/", ChangePasswordView.as_view(), name="password-change"),
    path("", include(router.urls)),
]
