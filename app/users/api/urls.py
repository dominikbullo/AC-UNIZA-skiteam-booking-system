from django.urls import path
from users.api.views import CurrentUserAPIView, ProfileList

urlpatterns = [
    path("", CurrentUserAPIView.as_view(), name="current-user"),
]
