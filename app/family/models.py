from django.db import models

from users.models import User


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
