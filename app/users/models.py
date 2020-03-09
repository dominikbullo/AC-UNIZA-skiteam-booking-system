# from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import AbstractUser, Group
from django.db import models

from core.utils import USER_TYPE_CHOICES


class User(AbstractUser):
    preferred_locale = models.CharField(max_length=2, blank=True, null=True)
    is_parent = models.BooleanField(default=False)

    def __str__(self):
        return self.name_or_username

    @property
    def name_or_username(self):
        if self.email != "":
            return self.email
        return self.username


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=30)
    location = models.CharField(max_length=30, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    avatar = models.ImageField(null=True, blank=True)

    # USER_TYPE_CHOICES is from from core.utils import USER_TYPE_CHOICES because i using it at m,any locations
    user_type = models.PositiveSmallIntegerField(choices=USER_TYPE_CHOICES, null=True, blank=True)

    class Meta:
        ordering = ['user__date_joined']

    def __str__(self):
        return self.user.name_or_username

    @property
    def full_name(self):
        return "%s %s" % (self.user.first_name, self.user.last_name)
