from django.urls import path, include

from rest_framework.routers import DefaultRouter

from users.api.views import ProfileViewSet, UsersViewSet

router = DefaultRouter()
router.register(r"profiles", ProfileViewSet)
router.register(r"users", UsersViewSet)

urlpatterns = [
    path("", include(router.urls)),

    # path("user/avatar/", AvatarUpdateView.as_view(), name="avatar-update"),
    # path("user/full-info/", CurrentUserAPIView.as_view(), name="current-user"),
    # # I don't need to create token, because i already have it when creating user
    # path('create/', CreateUserView.as_view(), name='create'),
    # path('user/token/', CreateTokenView.as_view(), name='token'),
    # path('user/me/', ManageUserView.as_view(), name='me'),
]
