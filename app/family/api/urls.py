from django.urls import path, include
from rest_framework.routers import DefaultRouter

from family.api.views import FamilyViewSet, ParentViewSet, ChildViewSet

# https://www.django-rest-framework.org/api-guide/routers/
router = DefaultRouter()
router.register(r"families", FamilyViewSet, basename="family")
router.register(r"parents", ParentViewSet)
router.register(r"children", ChildViewSet)

app_name = 'family'

urlpatterns = [
    path("", include(router.urls)),
]
