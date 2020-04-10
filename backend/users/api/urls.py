from django.urls import path, include
from rest_framework.routers import DefaultRouter
from users.api.views import ProfileViewSet

app_name = 'users'

router = DefaultRouter()
router.register(r"profile", ProfileViewSet, basename="profile")
# TODO test if on frontend i am using old user URL
router.register(r"user", ProfileViewSet, basename="user")

urlpatterns = [
    path("", include(router.urls)),
]
