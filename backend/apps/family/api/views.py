from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.response import Response

from apps.events.models import Season
from apps.family.models import Family, Child
from apps.family.api.serializers import FamilySerializer, ChildSerializer

# https://github.com/LondonAppDeveloper/recipe-app-api/blob/master/app/recipe/views.py
from core.views import get_season_by_query


class FamilyViewSet(viewsets.ModelViewSet):
    # TODO permissions
    queryset = Family.objects.all()
    serializer_class = FamilySerializer
    filter_backends = [SearchFilter]
    search_fields = ["name"]


class ChildViewSet(viewsets.ModelViewSet):
    # TODO permissions
    queryset = Child.objects.all()
    serializer_class = ChildSerializer

    # Sending parent of child (user which created him)
    def perform_create(self, serializer):
        serializer.save(parent=self.request.user)
