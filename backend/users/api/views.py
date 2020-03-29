from allauth.account.models import EmailConfirmation, EmailConfirmationHMAC
from allauth.socialaccount.providers.facebook.views import FacebookOAuth2Adapter

from django.contrib.auth import get_user_model
from django.http import HttpResponseRedirect

from rest_auth.registration.views import SocialLoginView

from rest_framework import generics, mixins, viewsets
from rest_framework.filters import SearchFilter
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView

from users.api.permissions import IsOwnProfileOrReadOnly
from users.api.serializers import ProfileAvatarSerializer, DetailProfileSerializer, UserDisplaySerializer

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
    permission_classes = [IsAuthenticated, IsOwnProfileOrReadOnly]
    filter_backends = [SearchFilter]
    search_fields = ["user"]


class UsersViewSet(mixins.UpdateModelMixin,
                   mixins.ListModelMixin,
                   mixins.RetrieveModelMixin,
                   viewsets.GenericViewSet):
    """ Used when changing info about user """
    queryset = get_user_model().objects.all()
    serializer_class = UserDisplaySerializer
    filter_backends = [SearchFilter]
    search_fields = ["username"]


class FacebookLogin(SocialLoginView):
    adapter_class = FacebookOAuth2Adapter


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
