from django.urls import path, include
from rest_framework.routers import DefaultRouter
from users.api.views import ProfileViewSet, UsersViewSet

app_name = 'users'

router = DefaultRouter()
router.register(r"profiles", ProfileViewSet, basename="profile")
router.register(r"users", UsersViewSet, basename="user")

urlpatterns = [
    path("", include(router.urls)),
]
