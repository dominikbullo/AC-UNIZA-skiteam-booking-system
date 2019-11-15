from django.urls import path
from users.api.views import *

urlpatterns = [
    path("", CurrentUserAPIView.as_view(), name="current-user"),
    path('create/', CreateUserView.as_view(), name='create'),
    path('token/', CreateTokenView.as_view(), name='token'),
    path('me/', ManageUserView.as_view(), name='me'),
]
