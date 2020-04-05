from allauth.account.models import EmailConfirmation, EmailConfirmationHMAC
from django.contrib.auth import get_user_model
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404

from rest_framework import generics, mixins, viewsets, filters
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from events.models import Season
from users.api.permissions import IsOwnProfileOrReadOnly
from users.api.serializers import (ProfileAvatarSerializer, DetailProfileSerializer, UserDetailSerializer,
                                   UserStatSerializer)

from users.models import Profile


class AvatarUpdateView(generics.UpdateAPIView):
    serializer_class = ProfileAvatarSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        profile_object = self.request.user.profile
        return profile_object


class ProfileViewSet(mixins.UpdateModelMixin,
                     mixins.ListModelMixin,
                     mixins.RetrieveModelMixin,
                     viewsets.GenericViewSet):
    """ Will be used when all users can see each other """
    queryset = Profile.objects.all()
    serializer_class = DetailProfileSerializer
    # permission_classes = [IsAuthenticated, IsOwnProfileOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ['user__username']

    def retrieve(self, request, *args, **kwargs):
        instance = get_object_or_404(Profile, user__username=kwargs["pk"])
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    # RES: https://stackoverflow.com/questions/36365326/django-rest-framework-doesnt-serialize-serializermethodfield
    # RES(filtering): https://stackoverflow.com/questions/26595906/django-rest-framework-with-viewset-router-queryset-filtering
    @action(detail=True, methods=['get'], url_path='stats')
    def get_stats(self, request, *args, **kwargs):
        user = get_object_or_404(Profile, user__username=kwargs["pk"])
        seasons = Season.objects.all()

        query = self.request.query_params.get('season')
        if query:
            if query == "current":
                seasons = seasons.filter(current=True)
            else:
                seasons = seasons.filter(pk=query)

        serializer = UserStatSerializer(instance={
            'user'   : user,
            'seasons': seasons,
        })
        return Response(serializer.data)


# class UsersViewSet(mixins.UpdateModelMixin,
#                    mixins.ListModelMixin,
#                    mixins.RetrieveModelMixin,
#                    viewsets.GenericViewSet):
#     """ Used when changing info about user """
#     queryset = get_user_model().objects.all()
#     serializer_class = UserDetailSerializer
#     filter_backends = [filters.SearchFilter]
#     search_fields = ["username"]


# RES: https://stackoverflow.com/questions/53305849/django-rest-auth-key-error-on-email-confirmation
class CustomConfirmEmailView(APIView):
    # TODO handle success and failure

    permission_classes = [AllowAny]

    def get(self, *args, **kwargs):
        self.object = confirmation = self.get_object()
        confirmation.confirm(self.request)
        # A React Router Route will handle the failure scenario
        return HttpResponseRedirect('/login/success')

    def get_object(self, queryset=None):
        key = self.kwargs['key']
        email_confirmation = EmailConfirmationHMAC.from_key(key)
        if not email_confirmation:
            if queryset is None:
                queryset = self.get_queryset()
            try:
                email_confirmation = queryset.get(key=key.lower())
            except EmailConfirmation.DoesNotExist:
                # A React Router Route will handle the failure scenario
                return HttpResponseRedirect('/login/failure/')
        return email_confirmation

    def get_queryset(self):
        qs = EmailConfirmation.objects.all_valid()
        qs = qs.select_related("email_address__user")
        return qs
