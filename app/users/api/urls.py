from django.urls import path
from users.api.views import *

urlpatterns = [
    path("", CurrentUserAPIView.as_view(), name="current-user"),

    # I don't need to create token, because i already have it when creating user
    # path('create/', CreateUserView.as_view(), name='create'),
    path('token/', CreateTokenView.as_view(), name='token'),
    path('me/', ManageUserView.as_view(), name='me'),
]
