from django.contrib.auth.models import AbstractUser, Group
from django.db import models

# class Family(models.Model):
#     id = models.AutoField(primary_key=True)
from django.utils import timezone


class User(AbstractUser):
    # User have some basic info
    # All users in system should be users

    # family_name = models.ForeignKey(Family, on_delete=models.CASCADE)
    # family_name = "testfamily"
    USER_TYPE_CHOICES = (
        (1, 'child'),
        (2, 'parent'),
        (3, 'coach'),
        (4, 'admin'),
    )
    #
    user_type = models.PositiveSmallIntegerField(choices=USER_TYPE_CHOICES, default=1)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    created_date = models.DateTimeField(default=timezone.now)
    bio = models.CharField(max_length=240, blank=True)
    city = models.CharField(max_length=30, blank=True)

    # avatar = models.ImageField(null=True, blank=True)

    def __str__(self):
        return self.user.username


class ProfileStatus(models.Model):
    user_profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    status_content = models.CharField(max_length=240)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "statuses"

    def __str__(self):
        return str(self.user_profile)


class FamilyMember(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    relationship = models.CharField(max_length=100)


class Parent(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    children = models.ManyToManyField('self', null=True, blank=True, related_name='c', symmetrical=False)


class Child:
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    parents = models.ManyToManyField('self', null=True, blank=True, related_name='p', symmetrical=False)
    pass


class Coach:
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
