from allauth.socialaccount.providers.facebook.views import FacebookOAuth2Adapter
from django.contrib.auth import get_user_model

from rest_auth.registration.views import SocialLoginView
from rest_framework import generics, mixins, viewsets
from rest_framework.permissions import IsAuthenticated

from rest_framework.filters import SearchFilter

from users.api.serializers import (ProfileAvatarSerializer, ProfileSerializer, CustomRegisterSerializer,
                                   UserDisplaySerializer)
from users.api.permissions import IsOwnerOrReadOnly, IsOwnProfileOrReadOnly
from users.models import Profile

from rest_framework import generics, authentication, permissions


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
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated, IsOwnProfileOrReadOnly]
    filter_backends = [SearchFilter]
    search_fields = ["user"]


class UsersViewSet(mixins.UpdateModelMixin,
                   mixins.ListModelMixin,
                   mixins.RetrieveModelMixin,
                   viewsets.GenericViewSet):
    queryset = get_user_model().objects.all()
    serializer_class = UserDisplaySerializer
    permission_classes = [IsAuthenticated, IsOwnProfileOrReadOnly]
    filter_backends = [SearchFilter]
    search_fields = ["user"]


class FacebookLogin(SocialLoginView):
    adapter_class = FacebookOAuth2Adapter

# from rest_auth.registration.views import SocialLoginView
# from allauth.socialaccount.providers.google.views import GoogleOAuth2RestAdapter
#
# # https://github.com/Tivix/django-rest-auth/issues/403
# class GoogleLogin(SocialLoginView):
#     adapter_class = GoogleOAuth2RestAdapter
