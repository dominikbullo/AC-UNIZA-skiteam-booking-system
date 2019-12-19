from django.http import Http404
from rest_framework import status
from rest_framework import mixins, viewsets
from rest_framework.response import Response
from rest_framework.filters import SearchFilter

from family.models import Family, Parent, Child
from family.api.serializers import FamilySerializer, ParentSerializer, ChildSerializer


class BaseRecipeAttrViewSet(viewsets.ModelViewSet):
    """Base viewset for user owned recipe attributes"""

    # authentication_classes = (TokenAuthentication,)
    # permission_classes = (IsAuthenticated,)

    # def get_queryset(self):
    #     """Return objects for the current authenticated user only"""
    #     assigned_only = bool(
    #         int(self.request.query_params.get('assigned_only', 0))
    #     )
    #     queryset = self.queryset
    #     if assigned_only:
    #         queryset = queryset.filter(recipe__isnull=False)
    #
    #     return queryset.filter(
    #         user=self.request.user
    #     ).order_by('-name').distinct()

    def perform_create(self, serializer):
        """Create a new object"""
        serializer.save()

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            self.perform_destroy(instance)
        except Http404:
            pass
        return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_destroy(self, instance):
        instance.delete()


class FamilyViewSet(BaseRecipeAttrViewSet):
    queryset = Family.objects.all()
    serializer_class = FamilySerializer
    filter_backends = [SearchFilter]
    search_fields = ["id"]


class ParentViewSet(BaseRecipeAttrViewSet):
    queryset = Parent.objects.all()
    serializer_class = ParentSerializer

    # filter_backends = [SearchFilter]
    # search_fields = ["user"]


class ChildViewSet(BaseRecipeAttrViewSet):
    queryset = Child.objects.all()
    serializer_class = ChildSerializer
    # filter_backends = [SearchFilter]
    # search_fields = ["user"]
