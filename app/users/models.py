from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone

# REFS
# https://medium.com/@royprins/django-custom-user-model-email-authentication-d3e89d36210f
# https://docs.djangoproject.com/en/2.2/topics/auth/default/

# TODO: Send verification mail
# TODO: Redirect after reg to login
# TODO: Do not allow anything to show when not login

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _
from django.conf import settings


class User(AbstractUser):
    username = models.CharField(blank=True, null=True, max_length=50)
    email = models.EmailField(_('email address'), unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    def __str__(self):
        return "{}".format(self.email)


class Parent(User, AbstractUser):
    class Meta:
        permissions = [
            ("test_permision", "Can change the status of tasks"),
            ("close_task", "Can remove a task by setting its status as closed"),
        ]


class Child(User, AbstractUser):
    category = models.CharField(max_length=5)

    class Meta:
        permissions = [
            ("test_permision", "Can change the status of tasks"),
            ("close_task", "Can remove a task by setting its status as closed"),
        ]

    def __str__(self):
        return "{}".format(self.email)


class Coach(User, AbstractUser):
    class Meta:
        permissions = (
            ('blog_view', 'can view blog posts and categories'),
            ('blog_edit', 'can edit blog category and post'),
            ("support_view", "can view tickets"),
            ("support_edit", "can edit tickets"),
            ("activity_view", "can view recruiters, applicants, data, posts"),
            ("activity_edit", "can edit data"),
        )


class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')
    title = models.CharField(max_length=5)
    family = models.CharField(max_length=5)
    dob = models.DateField()
    address = models.CharField(max_length=255)
    country = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    zip = models.CharField(max_length=5)
    USER_TYPE_CHOICES = (
        (1, 'student'),
        (2, 'teacher'),
        (3, 'secretary'),
        (4, 'supervisor'),
        (5, 'admin'),
    )

    user_type = models.PositiveSmallIntegerField(choices=USER_TYPE_CHOICES)
