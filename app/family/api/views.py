from rest_framework import viewsets, generics, status, mixins
from rest_framework.filters import SearchFilter
from rest_framework.response import Response
from rest_framework.views import APIView

from family.models import Family, Parent, Child
from family.api.serializers import FamilySerializer, ParentSerializer, ChildSerializer
from family.api.permissions import IsOwnerOrReadOnly, IsOwnFamilyOrReadOnly


# https://github.com/LondonAppDeveloper/recipe-app-api/blob/master/app/recipe/views.py
class FamiliesViewSet(viewsets.ModelViewSet):
    # TODO permissions
    queryset = Family.objects.all()
    serializer_class = FamilySerializer
    # permission_classes = [IsOwnFamilyOrReadOnly]
    filter_backends = [SearchFilter]
    search_fields = ["name"]


class ParentsViewSet(mixins.UpdateModelMixin,
                     mixins.ListModelMixin,
                     mixins.RetrieveModelMixin,
                     viewsets.GenericViewSet):
    # TODO permissions
    queryset = Parent.objects.all()
    serializer_class = ParentSerializer
    filter_backends = [SearchFilter]
    search_fields = ["user"]


class ChildrenViewSet(viewsets.ModelViewSet):
    # TODO permissions
    queryset = Child.objects.all()
    serializer_class = ChildSerializer
    filter_backends = [SearchFilter]
    search_fields = ["user"]
