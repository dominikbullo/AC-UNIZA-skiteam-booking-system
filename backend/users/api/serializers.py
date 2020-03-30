from allauth.account.models import EmailAddress

from django.contrib.auth import get_user_model

from rest_auth.models import TokenModel
from rest_auth.registration.serializers import RegisterSerializer
from rest_framework import serializers, status
from rest_framework.response import Response

from core.choices import UserTypeChoices
from family.models import Family, FamilyMember, Child
from users.models import Profile


class BaseProfileSerializer(serializers.ModelSerializer):
    first_name = serializers.DateTimeField(source='user.first_name', read_only=True)
    last_name = serializers.DateTimeField(source='user.last_name', read_only=True)
    username = serializers.DateTimeField(source='user.username', read_only=True)
    family_id = serializers.SerializerMethodField()

    # RES: https://stackoverflow.com/questions/48073471/django-rest-framework-get-data-based-on-current-userid-token
    def get_family_id(self, instance):
        # TODO: Try catch
        try:
            member = FamilyMember.objects.get(user=instance.user)
            family_id = member.family_id
            return family_id
        except Exception as e:
            print(e)
            print("User does not have family!")
            pass
        return Response(data=self.data, status=status.HTTP_404_NOT_FOUND)

    class Meta:
        model = Profile
        fields = ("family_id", "first_name", "last_name", "username")
        read_only_fields = 'family_id', "user_role"


class DetailProfileSerializer(BaseProfileSerializer):
    email = serializers.DateTimeField(source='user.email', read_only=True)
    avatar = serializers.ImageField(read_only=True)

    family_id = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        # RELEASE: exclude id of profile
        # exclude = ('id', "user")
        exclude = ('id', "user",)
        read_only_fields = 'family_id', "user_role"


class RegisterProfileSerializer(serializers.ModelSerializer):
    user_role = serializers.ChoiceField(choices=UserTypeChoices.choices, required=True)

    class Meta:
        model = Profile
        fields = ("birth_date", "gender", "user_role")


class ProfileAvatarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ("avatar",)


class UserDisplaySerializer(serializers.ModelSerializer):
    """Serializer for the users object"""
    verified_email = serializers.SerializerMethodField()

    # https://stackoverflow.com/questions/41394761/the-create-method-does-not-support-writable-nested-fields-by-default
    profile = DetailProfileSerializer(read_only=True)

    def get_verified_email(self, obj):
        try:
            email_address = EmailAddress.objects.get(user_id=obj.id)
            return email_address.verified
        except EmailAddress.DoesNotExist:
            return None

    def update(self, instance, validated_data):
        # TODO custom update
        return instance

    class Meta:
        model = get_user_model()
        fields = (
            'id', 'email', "username", 'first_name', "last_name", "verified_email", "profile")
        # exclude = ("password", "last_login", "is_superuser", "is_staff", "is_active",)
        read_only_fields = 'id', 'verified_email', "email",


class CustomRegisterSerializer(RegisterSerializer):
    username = serializers.CharField(read_only=True, required=False)
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)

    # Fixed KeyError events with custom serializer without this field
    profile = RegisterProfileSerializer(required=True)

    # FIXME get cleaned data -> normalize_email(email)
    def get_cleaned_data(self):
        default = super(CustomRegisterSerializer, self).get_cleaned_data()
        mine = {
            'first_name': self.validated_data.get('first_name', ''),
            'last_name' : self.validated_data.get('last_name', ''),
        }

        return {**default, **mine}

    def custom_signup(self, request, user):
        profile_data = request.data.pop('profile')
        Profile.objects.get_or_create(user=user, **profile_data)
        user.profile.save()

        # TODO family_creator only if parent
        family = Family.objects.create(name=user.email)
        family.save()

        parent = FamilyMember.objects.create(user=user, family=family)
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
