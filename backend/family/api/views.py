from rest_framework import viewsets, mixins
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from family.models import Family, FamilyMember, Child
from family.api.serializers import FamilySerializer, FamilyMemberSerializer, ChildSerializer

from family.api.permissions import IsOwnerOrReadOnly, IsOwnFamilyOrReadOnly


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
    filter_backends = [SearchFilter]
    search_fields = ["user"]

    def retrieve(self, request, *args, **kwargs):
        """
        This will retrieve child by username not by id
        :return: Child serializer data
        """
        instance = get_object_or_404(Child, user__username=kwargs["pk"])
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    # VIEW because i need to know user who is in the request
    # RES: https://stackoverflow.com/questions/34797050/django-rest-framework-create-child-of-nested-relationship
    # RES: https://stackoverflow.com/questions/41094013/when-to-use-serializers-create-and-modelviewsets-create-perform-create
    # RES: https://stackoverflow.com/questions/58437374/django-rest-auth-calling-registerview-from-other-viewset-sensitive-post-parame

    # Sending parent of child (user which created him)
    def perform_create(self, serializer):
        serializer.save(parent=self.request.user)
