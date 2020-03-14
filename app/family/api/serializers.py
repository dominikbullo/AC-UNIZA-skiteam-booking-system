from collections import OrderedDict

from allauth.account.adapter import get_adapter
from allauth.account.utils import setup_user_email
from django.contrib.auth import get_user_model
from rest_framework import serializers
from family.models import Child, Parent, Family

from users.api.serializers import CustomRegisterSerializer
from users.models import Profile


class CustomRegisterChildSerializer(CustomRegisterSerializer):
    # TODO on validation i can create username from email, but this is fine for now
    username = serializers.CharField(required=True)
    email = serializers.CharField(required=False)

    # https://github.com/Tivix/django-rest-auth/issues/464
    def get_cleaned_data(self):
        return {
            'name'    : self.validated_data.get('name', ''),
            'password': self.validated_data.get('password1', ''),
            'email'   : self.validated_data.get('email', '')
        }


# https://stackoverflow.com/questions/33659994/django-rest-framework-create-user-and-user-profile
class ChildSerializer(serializers.ModelSerializer):
    user = CustomRegisterChildSerializer(required=True)

    family = serializers.HyperlinkedRelatedField(read_only=True, view_name="family-detail")

    def create(self, validated_data):
        profile_data = validated_data["user"].pop('profile')
        password = validated_data["user"].pop('password1')
        # self.validated_data.get('name', '')
        validated_data["user"].pop('password2')

        user = get_user_model().objects.create(**validated_data["user"])
        user.set_password(password)
        user.save()

        Profile.objects.create(user=user, **profile_data)
        user.profile.save()

        try:
            print("Parent is:", validated_data["parent"])
        except:
            print("youre fucked")

        # TODO Here i can add user/owner/family
        child = Child.objects.create(user=user, family_id=1)
        return child

    class Meta:
        model = Child
        fields = "__all__"
        extra_kwargs = {'password': {'write_only': True, 'min_length': 5},
                        "username": {"required": True}}


class ParentSerializer(serializers.ModelSerializer):
    # I dont need that for now, because, i wil be searching family. Because if parent have all child,
    # then all parents must have these child and when I want to merge Mother and Father into one family, i just change
    # one of them family id. with all child if they have some
    # children = serializers.HyperlinkedRelatedField(many=True,
    #                                                read_only=True,
    #                                                view_name="child-detail")

    # user = serializers.StringRelatedField(read_only=True)
    user = serializers.HyperlinkedRelatedField(read_only=True, view_name="profile-detail")
    family = serializers.StringRelatedField()

    # def validate(self, data):
    #     raise serializers.ValidationError('Not a multiple of ten')

    # More possible ways
    # user = UserDisplaySerializer(read_only=True)
    # def create(self, validated_data):
    #     create_user()

    class Meta:
        model = Parent
        fields = "__all__"


class FamilySerializer(serializers.ModelSerializer):
    # parents = ParentSerializer(many=True, read_only=True)
    parents = serializers.HyperlinkedRelatedField(many=True,
                                                  read_only=True,
                                                  view_name="parent-detail")

    children = serializers.HyperlinkedRelatedField(many=True,
                                                   read_only=True,
                                                   view_name="child-detail")

    class Meta:
        model = Family
        fields = "__all__"
