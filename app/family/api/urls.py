from django.urls import path, include
from rest_framework.routers import DefaultRouter

from family.api.views import (FamilyListCreateAPIView,
                              ParentListCreateAPIView, ParentDetailAPIView,
                              ChildListCreateAPIView, ChildDetailAPIView)

# router = DefaultRouter()
# router.register(r"parents", ParentListCreateAPIView, base_name='parents')
# router.register(r"children", ChildListCreateAPIView, base_name='children')

urlpatterns = [
    # path("", include(router.urls)),
    path("", FamilyListCreateAPIView.as_view(), name="family-list"),
    # path("<int:pk>/", FamilyDetailAPIView.as_view(), name="family-detail"),

    path("parents/", ParentListCreateAPIView.as_view(), name="parent-list"),
    path("parents/<int:pk>/", ParentDetailAPIView.as_view(), name="parent-detail"),

    path("children/", ChildListCreateAPIView.as_view(), name="child-list"),
    path("children/<int:pk>/", ChildDetailAPIView.as_view(), name="child-detail"),
]
