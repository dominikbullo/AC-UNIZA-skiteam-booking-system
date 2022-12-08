# https://github.com/LondonAppDeveloper/recipe-app-api/blob/master/app/recipe/views.py
from core.views import get_season_by_query
from django.db import transaction
from django.utils.crypto import get_random_string
from rest_framework import generics, mixins, viewsets
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from sportagenda.apps.events.models import Season
from sportagenda.apps.family.api.serializers import (ChildSerializer,
                                                     FamilyMemberSerializer,
                                                     FamilySerializer)
from sportagenda.apps.family.models import Child, Family, FamilyMember


class FamilyViewSet(viewsets.ModelViewSet):
    # TODO permissions
    # TODO filter only user family
    # TODO: permission, is family member
    serializer_class = FamilySerializer
    queryset = Family.objects.all()
    filter_backends = [SearchFilter]
    search_fields = ["name"]

    @action(detail=True, methods=["get"], url_path="token")
    def get_family_token(self, obj, pk=None):
        family = self.get_object()
        family.token = get_random_string(length=64)
        family.save()
        return Response({"token": family.token})


class ChildViewSet(viewsets.ModelViewSet):
    # TODO permissions
    queryset = Child.objects.all()
    serializer_class = ChildSerializer

    # Sending parent of child (user which created_at him)
    def perform_create(self, serializer):
        serializer.save(parent=self.request.user)


class AddToFamilyView(APIView):
    serializer_class = FamilySerializer

    @transaction.atomic
    def get(self, request, token):
        """
        :param request:
        :param token:
        :return: Returning how family should look like after merging
        """
        ret = {}
        new_data = []

        mew_family = get_object_or_404(Family, token=token)
        print(f"Found new family {mew_family} with token {token}")

        family_member = get_object_or_404(FamilyMember, user=request.user)

        old_family = get_object_or_404(Family, id=family_member.family.id)
        user_old_family_members = FamilyMember.objects.filter(
            family=family_member.family
        )

        print(f"Old family {old_family}")
        ret.update({"old": self.serializer_class(old_family).data})
        # Good until now

        print(f"Found {len(user_old_family_members)} family member of requested user")

        print(f"new family {mew_family}")
        ret.update({"new": self.serializer_class(mew_family).data})
        return Response(ret)

    def post(self, request, token):
        """
        :param request:
        :param token:
        :return: Merged family
        """
        # ATTENTION: This is one time only operation, token will be destroyed after get request for safety!
        mew_family = get_object_or_404(Family, token=token)
        mew_family.token = None
        mew_family.save()

        print(f"Found family with token {token}")
        family_member = get_object_or_404(FamilyMember, user=request.user)
        print(family_member.family.id)
        user_old_family_members = FamilyMember.objects.filter(
            family=family_member.family
        )
        print("*****************")
        print(user_old_family_members)
        print(f"Found {len(user_old_family_members)} family member of requested user")
        for member in user_old_family_members:
            print("before", member.family.id)
            print("member", member)
            member.family = mew_family
            print("after", member.family.id)
            member.save()

        old_family = get_object_or_404(Family, id=family_member.family.id)
        old_family.delete()

        return Response(self.serializer_class(mew_family).data)
