from allauth.account.utils import setup_user_email, send_email_confirmation
from django.contrib.auth import get_user_model
from rest_framework import serializers
from family.models import Child, FamilyMember, Family

from users.api.serializers import CustomRegisterSerializer, UserDisplaySerializer
from users.models import Profile


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
        profile_data = validated_data["user"].pop('profile')
        password = validated_data["user"].pop('password1')
        validated_data["user"].pop('password2')

        user = get_user_model().objects.create(**validated_data["user"])
        user.set_password(password)
        user.save()

        if validated_data["user"].get("email", None):

            # TODO add email adress
            setup_user_email(self.context['request'], user, [])
            send_email_confirmation(self.context['request'], user, signup=False)
            # user.add_email_address(self.context['request'], validated_data["user"]["email"])

            # TODO singals
            Profile.objects.get_or_create(user=user, **profile_data)
            user.profile.save()

            # TODO Here i can add user/owner/family
            # RELEASE: Delete
        try:
            print("Parent is:", validated_data["parent"])
        except:
            print("youre fucked")

        if not validated_data.get("parent", None):
            # TODO doesn't pass parent
            return None

        parent = FamilyMember.objects.get(user=validated_data.get("parent"))

        # TODO doesn't found parent
        child = Child.objects.create(user=user, family_id=parent.family_id)
        # # TODO try save there
        # user.save()
        # user.profile.save()
        child.save()
        return child

    class Meta:
        model = Child
        fields = "__all__"
        extra_kwargs = {'password': {'write_only': True, 'min_length': 5},
                        "username": {"required": True}}


class FamilyMemberSerializer(serializers.ModelSerializer):
    user = UserDisplaySerializer(read_only=True)

    # user = serializers.HyperlinkedRelatedField(read_only=True, view_name="users:user-detail")

    class Meta:
        model = FamilyMember
        fields = "__all__"


class FamilySerializer(serializers.ModelSerializer):
    members = FamilyMemberSerializer(many=True, read_only=True)

    # children = ChildSerializer(many=True, read_only=True)

    class Meta:
        model = Family
        fields = "__all__"