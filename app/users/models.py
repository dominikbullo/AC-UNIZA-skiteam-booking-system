from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import AbstractUser, Group, PermissionsMixin
from django.db import models

from app import settings
from core.utils import USER_TYPE_CHOICES, GENDER_CHOICES


# https://github.com/LondonAppDeveloper/recipe-app-api/blob/master/app/core/models.py
# https://www.oodlestechnologies.com/blogs/How-to-Edit-User-Profile-Both-Django-User-and-Custom-User-Fields/
# https://www.codingforentrepreneurs.com/blog/how-to-create-a-custom-django-user-model
# TODO 13.03 -> this would be problem
class UserManager(BaseUserManager):
    # This creating user for child
    def create_user(self, username, email, password=None, **extra_fields):
        """Creates and saves a new user"""
        if not username:
            raise ValueError('Users must have an username')

        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_child_user(self, email, password1=None, **extra_fields):
        """Creates and saves a new user"""
        # TODO set user role
        user_payload = {
            "first_name": extra_fields['first_name'],
            "last_name" : extra_fields['last_name'],
        }

        user = self.create_user(
            email,
            password=password1,
            **user_payload
        )
        user.save(using=self._db)
        return user

    def create_staff_user(self, email, password, **extra_fields):
        """
        Creates and saves a staff user with the given email and password.
        """
        user = self.create_user(
            email,
            password=password,
            **extra_fields
        )
        user.staff = True
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password):
        """Creates and saves a new super user"""
        user = self.create_user(username, email, password)
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

    objects = UserManager()

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
