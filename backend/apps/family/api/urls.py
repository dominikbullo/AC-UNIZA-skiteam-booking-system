from apps.family.api.views import AddToFamilyView, ChildViewSet, FamilyViewSet
from django.urls import path
from rest_framework.routers import DefaultRouter

app_name = "family"

# https://www.django-rest-framework.org/api-guide/routers/
router = DefaultRouter()
router.register(r"family", FamilyViewSet, basename="family")
router.register(r"families", FamilyViewSet, basename="families")
router.register(r"child", ChildViewSet, basename="child")
router.register(r"children", ChildViewSet, basename="children")

urlpatterns = [
    path("family/add/<str:token>", AddToFamilyView.as_view(), name="add-to-family"),
]
