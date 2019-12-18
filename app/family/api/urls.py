from django.urls import path, include
from rest_framework.routers import DefaultRouter, SimpleRouter

from family.api.views import (FamilyListCreateAPIView, FamilyViewSet,
                              ParentListCreateAPIView, ParentDetailAPIView,
                              ChildListCreateAPIView, ChildDetailAPIView, ParentViewSet, ChildViewSet)

# https://www.django-rest-framework.org/api-guide/routers/
router = DefaultRouter()
router.register(r"families", FamilyViewSet)
router.register(r"parents", ParentViewSet)
router.register(r"children", ChildViewSet)

urlpatterns = [
    path("", include(router.urls)),
    # path("family/", FamilyListCreateAPIView.as_view(), name="family-list"),
    # path("family/<int:pk>/", FamilyDetailAPIView.as_view(), name="family-detail"),

    # path("parents/", ParentListCreateAPIView.as_view(), name="parent-list"),
    # path("parents/<int:pk>/", ParentDetailAPIView.as_view(), name="parent-detail"),

    # path("children/", ChildListCreateAPIView.as_view(), name="child-list"),
    # path("children/<int:pk>/", ChildDetailAPIView.as_view(), name="child-detail"),
]
