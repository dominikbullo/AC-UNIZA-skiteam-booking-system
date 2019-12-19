from django.db import models

from users.models import User
from core.utils import FAMILY_RELATION_CHOICE


# RESOURCES
# https://www.youtube.com/watch?v=gf2-J9YOMcc&t=458s
# https://stackoverflow.com/questions/55006095/how-to-represent-a-family-relationship-in-django-using-manytomany-and-inlineform
# https://riptutorial.com/Download/django-rest-framework.pdf


class Family(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Families"
        ordering = ['id']


class Person(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)

    class Meta:
        abstract = True
        ordering = ['user__date_joined']


class Parent(Person):
    family = models.ForeignKey(Family, on_delete=models.CASCADE, related_name="parents")
    title = models.CharField(max_length=30, blank=True)

    def __str__(self):
        return self.user.username


class Child(Person):
    family = models.ForeignKey(Family, on_delete=models.CASCADE, related_name="children")

    # i need to add user when creating child, and then, create child, add to family of user which creating it, and
    # add this user as parent of this child
    # whaever goes here -> it appiers at reguest
    # test = models.CharField(max_length=30, blank=True)

    # parent = models.ForeignKey(Parent, on_delete=models.CASCADE, related_name='children')

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name_plural = "Children"
