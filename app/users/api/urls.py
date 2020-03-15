from django.urls import path, include

from rest_framework.routers import DefaultRouter

from users.api.views import ProfileViewSet, UsersViewSet

router = DefaultRouter()
router.register(r"profiles", ProfileViewSet, basename="profile-list")
router.register(r"users", UsersViewSet, basename="user-list")

urlpatterns = [
    path("", include(router.urls)),
]
