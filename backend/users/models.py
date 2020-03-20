from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import AbstractUser, Group, PermissionsMixin
from django.db import models

from core.utils import USER_TYPE_CHOICES, GENDER_CHOICES


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

    def __str__(self):
        return self.name_or_username

    @property
    def name_or_username(self):
        if self.email != "":
            return self.email
        return self.username

    @property
    def full_name(self):
        return "%s %s" % (self.first_name, self.last_name)

    @property
    def display_name(self):
        return "%s %s" % (self.first_name, self.last_name)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=30, blank=True)
    location = models.CharField(max_length=30, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    avatar = models.ImageField(null=True, blank=True)

    # USER_TYPE_CHOICES is from from core.utils import USER_TYPE_CHOICES because i using it at m,any locations
    # user_type = models.PositiveSmallIntegerField(choices=USER_TYPE_CHOICES, null=True, blank=True)
    gender = models.CharField(choices=GENDER_CHOICES, max_length=1)

    class Meta:
        ordering = ['user__date_joined']

    def __str__(self):
        return self.user.name_or_username
