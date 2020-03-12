from django.contrib.auth import get_user_model
from rest_framework import serializers
from family.models import Child, Parent, Family

from users.api.serializers import CustomRegisterChildSerializer, ProfileSerializer


class ChildSerializer(serializers.ModelSerializer):
    user = CustomRegisterChildSerializer(required=True)

    family = serializers.HyperlinkedRelatedField(read_only=True,
                                                 view_name="family-detail")

    def create(self, validated_data):
        print("validated_data", validated_data)
        try:
            if validated_data["user"]["username"]:
                print("with username")
        except KeyError:
            if validated_data["user"]["email"] == "":
                print("with username and email")
                raise serializers.ValidationError('Email or Username is required')

        # TODO Add family as parent
        # # TODO doesnt have mail -> disable verification
        # if validated_data["user"]["email"] == "" and validated_data["user"]["username"] == "":
        validated_data["user"]["username"] = "tes"

        user = get_user_model().objects.create_user(**validated_data["user"])
        return Child.objects.create(user=user, family_id=1)

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
