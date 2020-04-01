from django.urls import path, include
from rest_framework.routers import DefaultRouter

from family.api.views import FamilyViewSet, FamilyMemberViewSet, ChildViewSet, ChildStatisticAPIView

app_name = 'family'

# https://www.django-rest-framework.org/api-guide/routers/
router = DefaultRouter()
router.register(r"family", FamilyViewSet, basename="family")
router.register(r"family-member", FamilyMemberViewSet, basename="family-member")
router.register(r"child", ChildViewSet, basename="child")

urlpatterns = [
    path("", include(router.urls)),
    path("child/<int:child_id>/statistic/", ChildStatisticAPIView.as_view()),
]
