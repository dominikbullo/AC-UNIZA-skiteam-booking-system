from django.urls import path, include

from rest_framework.routers import DefaultRouter

from users.api.views import (ProfileViewSet, AvatarUpdateView,
                             CurrentUserAPIView, CreateTokenView, ManageUserView)

router = DefaultRouter()
router.register(r"profiles", ProfileViewSet)

urlpatterns = [
    path("", include(router.urls)),

    path("avatar/", AvatarUpdateView.as_view(), name="avatar-update"),
    # TODO not safe for now -> need testing
    path("full-info/", CurrentUserAPIView.as_view(), name="current-user"),
    # I don't need to create token, because i already have it when creating user
    # path('create/', CreateUserView.as_view(), name='create'),
    path('token/', CreateTokenView.as_view(), name='token'),
    path('me/', ManageUserView.as_view(), name='me'),
]
