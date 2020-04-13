from django.urls import path, include
from rest_framework.routers import DefaultRouter
from users.api.views import ProfileViewSet, AvatarUpdateView

app_name = 'users'

router = DefaultRouter()
router.register(r"profile", ProfileViewSet, basename="profile")
# FIXME everything to user
# router.register(r"user", UserViewSet, basename="user")

urlpatterns = [
    path("", include(router.urls)),
    path("profile/<int:pk>/avatar/", AvatarUpdateView.as_view(), name="avatar-update"),

]
