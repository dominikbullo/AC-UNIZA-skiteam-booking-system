from allauth.account.models import EmailAddress

from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

from rest_auth.models import TokenModel
from rest_auth.registration.serializers import RegisterSerializer
from rest_framework import serializers
from rest_framework.generics import get_object_or_404

from core.choices import UserTypeChoices
from apps.family.models import Family, FamilyMember
from apps.users.models import Profile


class BaseProfileSerializer(serializers.ModelSerializer):
    # Used on FE
    family_id = serializers.SerializerMethodField()
    displayName = serializers.CharField(source='user.full_name', read_only=True)
    username = serializers.CharField(source='user.username', read_only=True)
    userRole = serializers.CharField(source='user_role', read_only=True)

    # Used in updating
    first_name = serializers.CharField(source='user.first_name')
    last_name = serializers.CharField(source='user.last_name')
    email = serializers.EmailField(source='user.email')

    gender = serializers.CharField(source='get_gender_display')
    avatar = serializers.ImageField(read_only=True)

    def get_family_id(self, instance):
        try:
            return get_object_or_404(FamilyMember, user=instance.user).family_id
        except Exception as e:
            # FIXME: Cannot find family ID, cannot show /api/profile/ -> list
            #             #  probably it should be like events -> polymorphic
            print(e)
            print("User does not have family or is not family member!")
            return -1

    def update(self, instance, validated_data):
        """Update a user, setting the password correctly and return it"""
        user_data = validated_data.pop('user', None)
        user = instance.user

        if user_data:
            # TODO validate and test
            user.first_name = user_data.get('first_name', user.first_name)
            user.last_name = user_data.get('last_name', user.last_name)
            user.email = user_data.get('email', user.email)
            # user.username = user_data.get('username', user.username)
            user.save()

        profile = super().update(instance, validated_data)
        profile.save()

        return profile

    class Meta:
        model = Profile
        exclude = ("events", "location", "user",)
        read_only_fields = "id", "family_id", "user_role", "events"


class RegisterProfileSerializer(serializers.ModelSerializer):
    user_role = serializers.ChoiceField(choices=UserTypeChoices.choices, required=True)

    class Meta:
        model = Profile
        fields = ("id", "birth_date", "gender", "user_role")


class ProfileAvatarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ("avatar",)


class BaseUserSerializer(serializers.ModelSerializer):
    """Serializer for the users object"""
    verified_email = serializers.SerializerMethodField()

    # https://stackoverflow.com/questions/41394761/the-create-method-does-not-support-writable-nested-fields-by-default
    profile = BaseProfileSerializer(read_only=True)

    def get_verified_email(self, obj):
        try:
            email_address = EmailAddress.objects.get(user_id=obj.id)
            return email_address.verified
        except EmailAddress.DoesNotExist:
            return None

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
    user = BaseUserSerializer(many=False, read_only=True)  # this is add by myself.

    class Meta:
        model = TokenModel
        fields = ('key', 'user')


from django.contrib.auth import password_validation
from rest_framework import serializers


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(max_length=128, write_only=True, required=True)
    new_password1 = serializers.CharField(max_length=128, write_only=True, required=True)
    new_password2 = serializers.CharField(max_length=128, write_only=True, required=True)

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError(
                _('Your old password was entered incorrectly. Please enter it again.')
            )
        return value

    def validate(self, data):
        if data['new_password1'] != data['new_password2']:
            raise serializers.ValidationError({'new_password2': _("The two password fields didn't match.")})
        password_validation.validate_password(data['new_password1'], self.context['request'].user)
        return data

    def save(self, **kwargs):
        password = self.validated_data['new_password1']
        user = self.context['request'].user
        user.set_password(password)
        user.save()
        return user
