from rest_framework import serializers

from users.models import User, Profile, ProfileStatus


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


class ProfileStatusSerializer(serializers.ModelSerializer):
    user_profile = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = ProfileStatus
        fields = "__all__"
