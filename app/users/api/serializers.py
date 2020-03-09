from allauth.account.models import EmailAddress
from rest_auth.models import TokenModel
from rest_framework import serializers
from users.models import User, Profile

from django.contrib.auth import get_user_model, authenticate
from django.utils.translation import ugettext_lazy as _


class UserSerializer(serializers.ModelSerializer):
    """Serializer for the users object"""
    verified_email = serializers.SerializerMethodField()

    class Meta:
        model = get_user_model()
        fields = ('email', "username", 'password', "first_name", "last_name", "verified_email")
        extra_kwargs = {
            'password': {'write_only': True, 'min_length': 5},
            'username': {'read_only': True, }
        }

    def get_verified_email(self, obj):
        try:
            email_address = EmailAddress.objects.get(user_id=obj.id)
            return email_address.verified
        except EmailAddress.DoesNotExist:
            return None

    def create(self, validated_data):
        """Create a new user with encrypted password and return it"""
        return get_user_model().objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        """Update a user, setting the password correctly and return it"""
        password = validated_data.pop('password', None)
        user = super().update(instance, validated_data)

        if password:
            user.set_password(password)
            user.save()

        return user


class AuthTokenSerializer(serializers.Serializer):
    """Serializer for the user authentication object"""
    email = serializers.CharField()
    password = serializers.CharField(
        style={'input_type': 'password'},
        trim_whitespace=False
    )

    def validate(self, attrs):
        """Validate and authenticate the user"""
        email = attrs.get('email')
        password = attrs.get('password')

        user = authenticate(
            request=self.context.get('request'),
            username=email,
            password=password
        )
        if not user:
            msg = _('Unable to authenticate with provided credentials')
            raise serializers.ValidationError(msg, code='authentication')

        attrs['user'] = user
        return attrs


class UserDisplaySerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class ProfileSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    avatar = serializers.ImageField(read_only=True)

    class Meta:
        model = Profile
        fields = "__all__"


class ProfileAvatarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ("avatar",)


from rest_auth.registration.serializers import RegisterSerializer


class CustomRegisterSerializer(RegisterSerializer):
    # preferred_locale = serializers.CharField(
    #     required=False,
    #     max_length=2,
    # )

    def get_cleaned_data(self):
        data_dict = super().get_cleaned_data()
        data_dict['preferred_locale'] = self.validated_data.get('preferred_locale', '')
        return data_dict


class TokenSerializer(serializers.ModelSerializer):
    """
    Serializer for Token model.
    """
    user = UserSerializer(many=False, read_only=True)  # this is add by myself.

    class Meta:
        model = TokenModel
        fields = ('key', 'user')
