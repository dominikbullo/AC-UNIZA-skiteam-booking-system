from django.urls import path

from users.api.views import CurrentUserAPIView, ProfileList

urlpatterns = [
    path("user/", CurrentUserAPIView.as_view(), name="current-user"),
    path("profiles/", ProfileList.as_view(), name="profile-list")
]
