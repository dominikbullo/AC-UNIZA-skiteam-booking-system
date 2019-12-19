from rest_framework import serializers
from family.models import Child, Parent, Family


class ChildSerializer(serializers.ModelSerializer):
    # user = serializers.StringRelatedField(read_only=True)
    user = serializers.HyperlinkedRelatedField(read_only=True,
                                               view_name="profile-detail")
    family = serializers.HyperlinkedRelatedField(read_only=True,
                                                 view_name="family-detail")

    # family = serializers.StringRelatedField()

    def create(self, validated_data):
        print("Creating new child with name", validated_data["name"])
        print(validated_data)
        return Child.objects.create(**validated_data)

    class Meta:
        model = Child
        fields = "__all__"

    # def create(self, validated_data):
    #     subject = Child.objects.create(parent=validated_data['parent']['id'], child_name=validated_data['child_name'])
    #
    #     return subject


class ParentSerializer(serializers.ModelSerializer):
    # I dont need that for now, because, i wil be searching family. Because if parent have all child,
    # then all parents must have these child and when I want to merge Mother and Father into one family, i just change
    # one of them family id. with all child if they have some
    # children = serializers.HyperlinkedRelatedField(many=True,
    #                                                read_only=True,
    #                                                view_name="child-detail")

    # user = serializers.StringRelatedField(read_only=True)
    user = serializers.HyperlinkedRelatedField(read_only=True, view_name="profile-detail")
    family = serializers.StringRelatedField(read_only=True)

    # def validate(self, data):
    #     raise serializers.ValidationError('Not a multiple of ten')

    # More possible ways
    # user = UserDisplaySerializer(read_only=True)

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

# class ArticleSerializer(serializers.Serializer):
#     id = serializers.IntegerField(read_only=True)
#     author = serializers.CharField()
#     title = serializers.CharField()
#     description = serializers.CharField()
#     body = serializers.CharField()
#     location = serializers.CharField()
#     publication_date = serializers.DateField()
#     active = serializers.BooleanField()
#     created_at = serializers.DateTimeField(read_only=True)
#     updated_at = serializers.DateTimeField(read_only=True)
#
#     def create(self, validated_data):
#         print(validated_data)
#         return Article.objects.create(**validated_data)
#
#     def update(self, instance, validated_data):
#         instance.author = validated_data.get('author', instance.author)
#         instance.title = validated_data.get('title', instance.title)
#         instance.description = validated_data.get('description',
#                                                   instance.description)
#         instance.body = validated_data.get('body', instance.body)
#         instance.location = validated_data.get('location', instance.location)
#         instance.publication_date = validated_data.get('publication_data',
#                                                        instance.publication_date)
#         instance.active = validated_data.get('active', instance.active)
#         instance.save()
#         return instance
#
#     def validate(self, data):
#         """ check that description and title are different
#         https://www.django-rest-framework.org/api-guide/serializers/#object-level-validation
#         """
#         if data["title"] == data["description"]:
#             raise serializers.ValidationError("Title and Description must be different from one another!")
#         return data
#
#     def validate_title(self, value):
#         """ check that title is at least 60 chars long
#         https://www.django-rest-framework.org/api-guide/serializers/#field-level-validation
#         """
#         if len(value) < 60:
#             raise serializers.ValidationError("The title has to be at least 60 chars long!")
#         return value
