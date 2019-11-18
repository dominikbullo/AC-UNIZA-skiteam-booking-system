from django.db import models

from users.models import User
from core.utils import FAMILY_RELATION_CHOICE


# RESOURCES
# https://www.youtube.com/watch?v=gf2-J9YOMcc&t=458s
# https://stackoverflow.com/questions/55006095/how-to-represent-a-family-relationship-in-django-using-manytomany-and-inlineform


class Person123(models.Model):
    name = models.CharField(max_length=50)


class FamilyMember123(models.Model):
    person = models.ManyToManyField(Person123, through='PersonFamilyMember123')
    relationType = models.PositiveSmallIntegerField(choices=FAMILY_RELATION_CHOICE)


class PersonFamilyMember123(models.Model):
    person = models.ForeignKey(Person123, on_delete=models.CASCADE)
    related = models.ForeignKey(FamilyMember123, on_delete=models.CASCADE)


#
# class Person(models.Model):
#     name = ...
#     family_members = models.ManyToManyField('self', through="FamilyMemberRelationship",
#                                             through_fields=('person', 'relation'))
#
#
# class FamilyMemberRelationship(models.Model):
#     person = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='relationships')
#     related = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='reverse_relationships')
#     relation_type = models.CharField(max_length=3, choices=FAMILY_RELATION_CHOICE)


class Family(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Families"
        ordering = ['name']


class FamilyMember(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    # relationship = models.CharField(max_length=100)

    def __str__(self):
        return self.user.username


class Relationship(models.Model):
    # from=
    # to=
    family = models.ForeignKey(Family, on_delete=models.CASCADE)
    family_member = models.ForeignKey(FamilyMember, on_delete=models.CASCADE)

    def __str__(self):
        return self.family


class Parent(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    children = models.ManyToManyField('self', null=True, blank=True, related_name='c', symmetrical=False)

    def __str__(self):
        return self.user.username


class Child(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    parents = models.ManyToManyField('self', null=True, blank=True, related_name='p', symmetrical=False)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name_plural = "Children"


class Coach(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name_plural = "Coaches"
