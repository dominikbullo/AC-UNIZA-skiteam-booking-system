from rest_framework import viewsets, mixins, status
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from apps.events.api.serializers import UserStatSerializer
from apps.events.models import Season
from apps.family.models import Family, FamilyMember, Child
from apps.family.api.serializers import FamilySerializer, FamilyMemberSerializer, ChildSerializer
from apps.family.api.permissions import IsOwnerOrReadOnly, IsOwnFamilyOrReadOnly


# https://github.com/LondonAppDeveloper/recipe-app-api/blob/master/app/recipe/views.py
class FamilyViewSet(viewsets.ModelViewSet):
    # TODO permissions
    queryset = Family.objects.all()
    serializer_class = FamilySerializer
    # permission_classes = [IsOwnFamilyOrReadOnly]
    filter_backends = [SearchFilter]
    search_fields = ["name"]


class FamilyMemberViewSet(mixins.UpdateModelMixin,
                          mixins.ListModelMixin,
                          mixins.RetrieveModelMixin,
                          viewsets.GenericViewSet):
    # TODO permissions
    queryset = FamilyMember.objects.all()
    serializer_class = FamilyMemberSerializer
    filter_backends = [SearchFilter]
    search_fields = ["user"]


class ChildViewSet(viewsets.ModelViewSet):
    # TODO permissions
    queryset = Child.objects.all()
    serializer_class = ChildSerializer

    # filter_backends = [SearchFilter]
    # search_fields = ["user.username"]

    # Sending parent of child (user which created him)
    def perform_create(self, serializer):
        serializer.save(parent=self.request.user)

    @action(detail=False, methods=['get'], url_path='stats')
    def get_stats(self, request, *args, **kwargs):
        # TODO stat for every user in current season
        # user = get_object_or_404(Child, pk=kwargs["pk"]).user.profile

        query = self.request.query_params.get('season')
        seasons = self.get_season_by_query(query, Season.objects.all())
        print("find season", seasons)

        # serializer = UserStatSerializer(instance={
        #     'user'   : user,
        #     'seasons': seasons,
        # })

        return Response(status=status.HTTP_404_NOT_FOUND)

    @staticmethod
    def get_season_by_query(query, seasons):
        if query:
            if query == "current":
                seasons = seasons.filter(current=True)
            else:
                seasons = seasons.filter(year=query)
        return seasons
