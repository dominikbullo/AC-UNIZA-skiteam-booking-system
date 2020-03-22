from django.urls import path, include
from rest_framework.routers import DefaultRouter

from family.api.views import FamiliesViewSet, FamilyMemberViewSet, ChildrenViewSet

app_name = 'family'

# https://www.django-rest-framework.org/api-guide/routers/
router = DefaultRouter()
router.register(r"families", FamiliesViewSet, basename="family")
router.register(r"children", ChildrenViewSet, basename="child")

urlpatterns = [
    path("", include(router.urls)),
]
