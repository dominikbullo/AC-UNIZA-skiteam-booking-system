from allauth.account.models import EmailAddress
from allauth.account.utils import send_email_confirmation
from django.contrib.auth import get_user_model
from rest_framework import serializers

from apps.events.models import Category, Season
from apps.family.models import Child, Family, FamilyMember
from apps.users.api.serializers import BaseUserSerializer, CustomRegisterSerializer
from apps.users.models import Profile, User


class ChildProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="user.username", read_only=True)

    class Meta:
        model = Child
        fields = "__all__"


class CustomRegisterChildSerializer(CustomRegisterSerializer):
    # IDEA: on validation i can create username from email, but this is fine for now
    email = serializers.CharField(required=False, allow_blank=True)


class ChildSerializer(serializers.ModelSerializer):
    user = CustomRegisterChildSerializer(required=True)
    family = serializers.HyperlinkedRelatedField(read_only=True, view_name="family-detail")

    def create(self, validated_data):
        # TODO: Use allauth method for usernames if possible
        profile_data = validated_data["user"].pop("profile")

        # TODO on validation
        password = validated_data["user"].pop("password1")
        validated_data["user"].pop("password2")

        user_data = validated_data["user"]
        print(f"user_data {user_data}")

        username = str(user_data.get("first_name", "") + user_data.get("last_name", "")).lower()
        counter = 1
        while User.objects.filter(username=username):
            username = username + str(counter)
            counter += 1
        # RES: https://stackoverflow.com/questions/16664874/how-to-add-an-element-to-the-beginning-of-an-ordereddict
        user_data.update({"username": username})

        # RES: https://stackoverflow.com/questions/30085996/djangorestframework-registering-a-user-difference-between-userserializer-save
        user = get_user_model().objects.create_user(**user_data)
        user.set_password(password)
        user.save()

        # RES: https://stackoverflow.com/questions/29147550/how-do-i-create-a-proper-user-with-django-allauth
        if user_data.get("email", ""):
            EmailAddress.objects.create(
                user=user,
                email=user_data.get("email", ""),
                primary=True,
                verified=False,
            )
            send_email_confirmation(self.context.get("request"), user)

        Profile.objects.get_or_create(user=user, **profile_data)
        user.profile.save()

        # Get parent and create child
        parent = FamilyMember.objects.get(user=validated_data.get("parent"))
        child = Child.objects.create(user=user, family_id=parent.family_id)

        # Match categories for this child
        query_category = {
            "season": Season.objects.get(current=True),
            "year_from__lte": user.profile.birth_date.year,
            "year_until__gte": user.profile.birth_date.year,
        }
        matched_category = Category.objects.filter(**query_category)

        # Add matching category from current season to child
        child.categories.set(matched_category)

        child.save()
        return child

    class Meta:
        model = Child
        fields = "__all__"
        extra_kwargs = {
            "password": {"write_only": True, "min_length": 5},
        }


class FamilyMemberSerializer(serializers.ModelSerializer):
    user = BaseUserSerializer(read_only=True)

    class Meta:
        model = FamilyMember
        fields = "__all__"


class FamilySerializer(serializers.ModelSerializer):
    members = FamilyMemberSerializer(many=True, read_only=True)

    children = ChildSerializer(many=True, read_only=True)

    class Meta:
        model = Family
        fields = "__all__"
