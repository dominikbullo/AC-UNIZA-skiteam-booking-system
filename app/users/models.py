from django.contrib.auth.models import AbstractUser, Group
from django.db import models

from core.utils import USER_TYPE_CHOICES, GENDER_CHOICES


class User(AbstractUser):
    user_role = models.PositiveSmallIntegerField(choices=USER_TYPE_CHOICES, null=True, blank=True)

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
