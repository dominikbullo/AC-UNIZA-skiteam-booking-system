from django.db import models

from users.models import User
from core.utils import FAMILY_RELATION_CHOICE


# RESOURCES
# https://www.youtube.com/watch?v=gf2-J9YOMcc&t=458s
# https://stackoverflow.com/questions/55006095/how-to-represent-a-family-relationship-in-django-using-manytomany-and-inlineform
# https://riptutorial.com/Download/django-rest-framework.pdf

class Person(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    class Meta:
        abstract = True


class Family(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Families"
        ordering = ['name']


class FamilyMemberRelationship(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='relationships')
    related = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='reverse_relationships')
    relation_type = models.CharField(max_length=3, choices=FAMILY_RELATION_CHOICE)


class Parent(Person):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=30, blank=True)

    def __str__(self):
        return self.user.username


class Child(Person):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    parent = models.ForeignKey(Parent, on_delete=models.CASCADE, related_name='children')

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name_plural = "Children"
