from allauth.account.models import EmailAddress
from django.contrib.auth import get_user_model
from rest_auth.models import TokenModel
from rest_framework import serializers
from users.models import User, Profile
from rest_auth.registration.serializers import RegisterSerializer


class UserDisplaySerializer(serializers.ModelSerializer):
    """Serializer for the users object"""
    verified_email = serializers.SerializerMethodField()

    user_role = serializers.CharField(source='get_user_role_display')

    def get_verified_email(self, obj):
        try:
            email_address = EmailAddress.objects.get(user_id=obj.id)
            return email_address.verified
        except EmailAddress.DoesNotExist:
            return None

    class Meta:
        model = get_user_model()
        fields = ('email', "username", 'password', 'first_name', "last_name", "verified_email", "user_role")
        extra_kwargs = {
            'password': {'write_only': True, 'min_length': 5},
            'username': {'read_only': True},
        }


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


class CustomRegisterSerializer(RegisterSerializer):
    username = serializers.CharField(read_only=True, required=False)
    email = serializers.EmailField(required=True)
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    profile = ProfileSerializer(required=True)

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass

    def get_cleaned_data(self):
        super(CustomRegisterSerializer, self).get_cleaned_data()

        return {
            'email'        : self.validated_data.get('email', ''),
            'first_name'   : self.validated_data.get('first_name', ''),
            'last_name'    : self.validated_data.get('last_name', ''),
            'password1'    : self.validated_data.get('password1', ''),
            'date_of_birth': self.validated_data.get('date_of_birth', ''),
        }


class CustomRegisterChildSerializer(CustomRegisterSerializer):
    # TODO on validation i can create username from email, but this is fine for now
    username = serializers.CharField(required=True)
    email = serializers.EmailField(required=False)


class TokenSerializer(serializers.ModelSerializer):
    """
    Serializer for Token model.
    """
    user = UserDisplaySerializer(many=False, read_only=True)  # this is add by myself.

    class Meta:
        model = TokenModel
        fields = ('key', 'user')
