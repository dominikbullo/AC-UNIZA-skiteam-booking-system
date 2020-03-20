import datetime

from allauth.account.models import EmailAddress
from allauth.account.utils import setup_user_email

from django.contrib.auth import get_user_model

from rest_auth.models import TokenModel
from rest_auth.registration.serializers import RegisterSerializer
from rest_framework import serializers

from family.models import Family, Parent
from users.models import Profile


class ProfileSerializer(serializers.ModelSerializer):
    avatar = serializers.ImageField(read_only=True)

    def to_representation(self, instance):
        representation = super(ProfileSerializer, self).to_representation(instance)

        # Because i have date in DB as format YYYY-MM-DD, if i getting it i need to reformat
        # Same in login
        try:
            representation['birth_date'] = instance.birth_date.strftime("%d.%m.%Y")
        except AttributeError as e:
            print(e)
            print("User doesn't have birth date!")
        return representation

    class Meta:
        model = Profile
        # RELEASE: exclude id of profile
        # exclude = ('id', "user")
        exclude = ('id', "user")


class ProfileAvatarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ("avatar",)


class UserDisplaySerializer(serializers.ModelSerializer):
    """Serializer for the users object"""
    verified_email = serializers.SerializerMethodField()

    user_role = serializers.CharField(source='get_user_role_display')
    profile = ProfileSerializer(required=True)

    def get_verified_email(self, obj):
        try:
            email_address = EmailAddress.objects.get(user_id=obj.id)
            return email_address.verified
        except EmailAddress.DoesNotExist:
            return None

    class Meta:
        model = get_user_model()
        fields = (
            'id', 'email', "username", 'password', 'first_name', "last_name", "verified_email", "user_role", "profile")
        # exclude = ("password", "last_login", "is_superuser", "is_staff", "is_active",)
        extra_kwargs = {
            'password': {'write_only': True, 'min_length': 5},
            'username': {'read_only': True},
        }


class CustomRegisterSerializer(RegisterSerializer):
    username = serializers.CharField(read_only=True, required=False)
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)

    profile = ProfileSerializer(required=True)

    # FIXME get cleaned data -> normalize_email(email)
    def get_cleaned_data(self):
        default = super(CustomRegisterSerializer, self).get_cleaned_data()
        mine = {
            'first_name': self.validated_data.get('first_name', ''),
            'last_name' : self.validated_data.get('last_name', ''),
        }

        return {**default, **mine}

    def custom_signup(self, request, user):
        # TODO: ACCOUNT_EMAIL_VERIFICATION = 'mandatory'
        #       Don't create user on request only after mail verifications

        profile_data = request.data.pop('profile')
        # profile_data["birth_date"] = datetime.datetime.strptime(
        #     profile_data["birth_date"], '%d.%m.%Y').date().strftime('%Y-%m-%d')

        profile_data["birth_date"] = datetime.datetime.strptime(profile_data["birth_date"], '%d.%m.%Y').date()

        Profile.objects.create(user=user, **profile_data)
        user.profile.save()

        # TODO family_creator only if parent
        family = Family.objects.create(name=user.email)
        family.save()

        parent = Parent.objects.create(user=user, family=family)
        parent.save()

        # # TODO: Validate date of birthday only 18 +
        # def validate_date_of_birthday(self, date_of_birthday):
        #     age = relativedelta(datetime.now(), date_of_birthday).years
        #
        #     if age < 18:
        #         raise serializers.ValidationError('Must be at least 18 years old to register.')
        #     else:
        #         return date_of_birthday


class TokenSerializer(serializers.ModelSerializer):
    """
    Serializer for Token model.
    """
    user = UserDisplaySerializer(many=False, read_only=True)  # this is add by myself.

    class Meta:
        model = TokenModel
        fields = ('key', 'user')
