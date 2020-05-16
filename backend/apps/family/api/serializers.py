from allauth.account.utils import setup_user_email, send_email_confirmation
from django.contrib.auth import get_user_model
from rest_framework import serializers, status
from rest_framework.response import Response

from apps.events.models import Category, Season
from apps.family.models import Child, FamilyMember, Family

from apps.users.api.serializers import CustomRegisterSerializer, UserDetailSerializer
from apps.users.models import Profile


class ChildProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = Child
        fields = ("username",)
        # Could show child category
        # fields = ("username", "first_name", "last_name", "categories")


class CustomRegisterChildSerializer(CustomRegisterSerializer):
    # IDEA: on validation i can create username from email, but this is fine for now
    username = serializers.CharField(required=True)
    email = serializers.CharField(required=False, allow_blank=True)

    # RES: https://github.com/Tivix/django-rest-auth/issues/464
    def get_cleaned_data(self):
        return {
            'name'    : self.validated_data.get('name', ''),
            'password': self.validated_data.get('password1', ''),
            'email'   : self.validated_data.get('email', '')
        }


# RES: https://stackoverflow.com/questions/33659994/django-rest-framework-create-user-and-user-profile
class ChildSerializer(serializers.ModelSerializer):
    user = CustomRegisterChildSerializer(required=True)

    family = serializers.HyperlinkedRelatedField(read_only=True, view_name="family:family-detail")

    def create(self, validated_data):
        # TODO validated data ?
        profile_data = validated_data["user"].pop('profile')
        password = validated_data["user"].pop('password1')
        validated_data["user"].pop('password2')

        user = get_user_model().objects.create(**validated_data["user"])
        user.set_password(password)
        user.save()

        Profile.objects.get_or_create(user=user, **profile_data)
        user.profile.save()

        if not validated_data.get("parent", None):
            return Response(status=status.HTTP_400_BAD_REQUEST)

        # Get parent and create child
        parent = FamilyMember.objects.get(user=validated_data.get("parent"))
        child = Child.objects.create(user=user, family_id=parent.family_id)

        # Match categories for this child
        query_category = {
            "season"         : Season.objects.get(current=True),
            "year_from__lte" : user.profile.birth_date.year,
            "year_until__gte": user.profile.birth_date.year
        }
        matched_category = Category.objects.filter(**query_category)

        # Add matching category from current season to child
        child.categories.set(matched_category)

        child.save()
        return child

    class Meta:
        model = Child
        fields = "__all__"
        extra_kwargs = {'password': {'write_only': True, 'min_length': 5},
                        "username": {"required": True}}


class FamilyMemberSerializer(serializers.ModelSerializer):
    user = UserDetailSerializer(read_only=True)

    class Meta:
        model = FamilyMember
        fields = "__all__"


class FamilySerializer(serializers.ModelSerializer):
    members = FamilyMemberSerializer(many=True, read_only=True)

    children = ChildSerializer(many=True, read_only=True)

    class Meta:
        model = Family
        fields = "__all__"
