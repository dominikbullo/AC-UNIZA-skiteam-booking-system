from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser, Group, PermissionsMixin
from django.db import models

from app import settings
from core.utils import USER_TYPE_CHOICES, GENDER_CHOICES


# https://github.com/LondonAppDeveloper/recipe-app-api/blob/master/app/core/models.py
# https://www.oodlestechnologies.com/blogs/How-to-Edit-User-Profile-Both-Django-User-and-Custom-User-Fields/
class UserManager(BaseUserManager):

    def create_user(self, username, email=None, password=None, **extra_fields):
        """Creates and saves a new user"""

        if not username:
            raise ValueError('The given username must be set')

        user_payload = {
            "first_name": extra_fields['first_name'],
            "last_name" : extra_fields['last_name'],
        }

        username = self.model.normalize_username(username)

        user = self.model(username=username, email=email, **user_payload)
        user.set_password(password)
        user.save(using=self._db)

        user.profile.birth_date = extra_fields['profile']["birth_date"]
        user.profile.gender = extra_fields['profile']["gender"]
        user.profile.save()

        return user

    def create_superuser(self, email, password):
        """Creates and saves a new super user"""
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


# https://testdriven.io/blog/django-custom-user-model/
# https://simpleisbetterthancomplex.com/tutorial/2016/07/22/how-to-extend-django-user-model.html#onetoone
class User(AbstractUser):
    """
    Custom user model that supports using email or username
    Also require first and last name
    """
    first_name = models.CharField(max_length=50, null=False, blank=False)
    last_name = models.CharField(max_length=150, null=False, blank=False)

    user_role = models.PositiveSmallIntegerField(choices=USER_TYPE_CHOICES, null=True, blank=True)

    # objects = UserManager()

    def __str__(self):
        return self.name_or_username

    @property
    def name_or_username(self):
        if self.email != "":
            return self.email
        return self.username


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=30, blank=True)
    location = models.CharField(max_length=30, blank=True)
    birth_date = models.DateField(null=False, blank=False)
    avatar = models.ImageField(null=True, blank=True)

    # USER_TYPE_CHOICES is from from core.utils import USER_TYPE_CHOICES because i using it at m,any locations
    # user_type = models.PositiveSmallIntegerField(choices=USER_TYPE_CHOICES, null=True, blank=True)
    gender = models.CharField(choices=GENDER_CHOICES, max_length=1)

    class Meta:
        ordering = ['user__date_joined']

    def __str__(self):
        return self.user.name_or_username

    @property
    def full_name(self):
        return "%s %s" % (self.user.first_name, self.user.last_name)
