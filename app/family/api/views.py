from rest_framework import viewsets, mixins
from rest_framework.filters import SearchFilter

from family.models import Family, Parent, Child
from family.api.serializers import FamilySerializer, ParentSerializer, ChildSerializer, CustomRegisterChildSerializer
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

    # VIEW because i need to know user who is in the request
    # https://stackoverflow.com/questions/34797050/django-rest-framework-create-child-of-nested-relationship
    # https://stackoverflow.com/questions/41094013/when-to-use-serializers-create-and-modelviewsets-create-perform-create
    # https://stackoverflow.com/questions/58437374/django-rest-auth-calling-registerview-from-other-viewset-sensitive-post-parame

    # def create(self, request, *args, **kwargs):
    #     # user = Rei(self.request)
    #     # Create user
    #     # Create child(user=user, parent=request.user, family=request.user.family
    #     # return response
    #     pass

    # Sending parent of child (user which created him)
    def perform_create(self, serializer):
        serializer.save(parent=self.request.user)
