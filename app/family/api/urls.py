from django.urls import path, include
from rest_framework.routers import DefaultRouter

from family.api.views import FamilyListCreateAPIView, ParentListCreateAPIView, ChildListCreateAPIView

# router = DefaultRouter()
# router.register(r"profiles", ProfileViewSet)

urlpatterns = [
    # path("", include(router.urls)),
    path("", FamilyListCreateAPIView.as_view(), name="family-list"),
    path("parents/", ParentListCreateAPIView.as_view(), name="parent-list"),
    path("children/", ChildListCreateAPIView.as_view(), name="child-list"),
]
