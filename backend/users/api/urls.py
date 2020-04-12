from django.urls import path, include
from rest_framework.routers import DefaultRouter
from users.api.views import ProfileViewSet

app_name = 'users'

router = DefaultRouter()
router.register(r"profile", ProfileViewSet, basename="profile")
router.register(r"user", ProfileViewSet, basename="user")
# FIXME everything to user
# FIXME TODO
# router.register(r"userNewTest", UserViewSet, basename="userNewTest")

urlpatterns = [
    path("", include(router.urls)),
]
