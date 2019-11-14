# from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import AbstractUser, Group
from django.db import models

from core.utils import USER_TYPE_CHOICES


class User(AbstractUser):
    pass


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    location = models.CharField(max_length=30, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    phone_number = models.CharField(max_length=30, blank=True)

    # USER_TYPE_CHOICES is from from core.utils import USER_TYPE_CHOICES because i using it at m,any locations
    user_type = models.PositiveSmallIntegerField(choices=USER_TYPE_CHOICES, null=True, blank=True)

    def __str__(self):  # __unicode__ for Python 2
        return self.user.username


class Family(models.Model):
    id = models.AutoField(primary_key=True)


class FamilyMember(models.Model):
    profile = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    relationship = models.CharField(max_length=100)


class Parent(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    children = models.ManyToManyField('self', null=True, blank=True, related_name='c', symmetrical=False)

    def __str__(self):
        return self.user.username


class Child:
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    parents = models.ManyToManyField('self', null=True, blank=True, related_name='p', symmetrical=False)
    pass


class Coach:
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
