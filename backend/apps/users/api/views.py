from allauth.account.models import EmailConfirmation, EmailConfirmationHMAC
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import generics, mixins, viewsets, status
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import UpdateAPIView
from rest_framework.authtoken.models import Token

from apps.events.models import Season
from apps.events.api.serializers import ProfileStatSerializer

from apps.users.models import Profile
from apps.users.api.serializers import ProfileAvatarSerializer, ChangePasswordSerializer, BaseProfileSerializer
from core.views import get_object_custom_queryset, get_season_by_query


class AvatarUpdateView(generics.UpdateAPIView):
    serializer_class = ProfileAvatarSerializer

    def get_object(self):
        profile_object = self.request.user.profile
        return profile_object


# RES: https://stackoverflow.com/questions/38845051/how-to-update-user-password-in-django-rest-framework
class ChangePasswordView(UpdateAPIView):
    serializer_class = ChangePasswordSerializer

    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        # if using drf authtoken, create a new token
        if hasattr(user, 'auth_token'):
            user.auth_token.delete()
        token, created = Token.objects.get_or_create(user=user)
        # return new token
        return Response({'token': token.key}, status=status.HTTP_200_OK)


class ProfileViewSet(mixins.UpdateModelMixin,
                     mixins.ListModelMixin,
                     mixins.RetrieveModelMixin,
                     viewsets.GenericViewSet):
    """ Will be used when all users can see each other """
    queryset = Profile.objects.all()
    serializer_class = BaseProfileSerializer
    # permission_classes = [IsAuthenticated, IsOwnProfileOrReadOnly]

    __basic_fields = ('user__username', 'user_role', "gender")
    filter_backends = (DjangoFilterBackend, SearchFilter)
    filter_fields = __basic_fields
    search_fields = __basic_fields

    # RES: https://stackoverflow.com/questions/36365326/django-rest-framework-doesnt-serialize-serializermethodfield
    # RES(filtering): https://stackoverflow.com/questions/26595906/django-rest-framework-with-viewset-router-queryset-filtering
    @action(detail=True, methods=['get'], url_path='stats')
    def get_stats(self, request, *args, **kwargs):
        profile = get_object_or_404(Profile, pk=kwargs["pk"])

        # TODO refactor
        seasons = get_season_by_query(self.request, Season.objects.all())

        serializer = ProfileStatSerializer(instance={
            'user'   : profile,
            'seasons': seasons,
        })
        return Response(serializer.data)


# RES: https://stackoverflow.com/questions/53305849/django-rest-auth-key-error-on-email-confirmation
class CustomConfirmEmailView(APIView):
    # TODO handle success and failure
    permission_classes = [AllowAny]

    def get(self, *args, **kwargs):
        self.object = confirmation = self.get_object()
        confirmation.confirm(self.request)
        # A React Router Route will handle the failure scenario
        return HttpResponseRedirect('/login')

    def get_object(self, queryset=None):
        key = self.kwargs['key']
        email_confirmation = EmailConfirmationHMAC.from_key(key)
        if not email_confirmation:
            if queryset is None:
                queryset = self.get_queryset()
            try:
                email_confirmation = queryset.get(key=key.lower())
            except EmailConfirmation.DoesNotExist:
                # TODO: some page on FE to react to this
                return HttpResponseRedirect('/login/failure/')
        return email_confirmation

    def get_queryset(self):
        qs = EmailConfirmation.objects.all_valid()
        qs = qs.select_related("email_address__user")
        return qs
