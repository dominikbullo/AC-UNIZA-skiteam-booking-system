from rest_framework import viewsets, mixins, status
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from apps.events.api.serializers import UserStatSerializer
from apps.events.models import Season
from apps.family.api.permissions import IsOwnFamilyOrReadOnly
from apps.family.models import Family, FamilyMember, Child
from apps.family.api.serializers import FamilySerializer, FamilyMemberSerializer, ChildSerializer

# https://github.com/LondonAppDeveloper/recipe-app-api/blob/master/app/recipe/views.py
from core.permissions import IsCoachOrReadOnly


class FamilyViewSet(viewsets.ModelViewSet):
    # TODO permissions
    queryset = Family.objects.all()
    serializer_class = FamilySerializer
    permission_classes = [IsOwnFamilyOrReadOnly, IsCoachOrReadOnly]
    filter_backends = [SearchFilter]
    search_fields = ["name"]


class FamilyMemberViewSet(mixins.UpdateModelMixin,
                          mixins.ListModelMixin,
                          mixins.RetrieveModelMixin,
                          viewsets.GenericViewSet):
    # TODO permissions
    queryset = FamilyMember.objects.all()
    serializer_class = FamilyMemberSerializer
    permission_classes = [IsOwnFamilyOrReadOnly, IsCoachOrReadOnly]
    filter_backends = [SearchFilter]
    search_fields = ["user"]


class ChildViewSet(viewsets.ModelViewSet):
    # TODO permissions
    queryset = Child.objects.all()
    serializer_class = ChildSerializer
    permission_classes = [IsOwnFamilyOrReadOnly, IsCoachOrReadOnly]

    # filter_backends = [SearchFilter]
    # search_fields = ["user.username"]

    # Sending parent of child (user which created him)
    def perform_create(self, serializer):
        serializer.save(parent=self.request.user)

    @action(detail=False, methods=['get'], url_path='stats')
    def get_stats(self, request, *args, **kwargs):
        ret = []

        # TODO refactor
        seasons = get_season_by_query(self.request, Season.objects.all())

        for child in Child.objects.all():
            serializer = UserStatSerializer(instance={
                'user'   : child.user.profile,
                'seasons': seasons,
            })

            ret.append(serializer.data)

        return Response(ret)

    @staticmethod
    def get_season_by_query(query, seasons):
        if query:
            if query == "current":
                seasons = seasons.filter(current=True)
            else:
                seasons = seasons.filter(year=query)
        return seasons
