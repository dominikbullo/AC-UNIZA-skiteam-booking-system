from django.db import models

from users.models import User


class Family(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class FamilyMember(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    relationship = models.CharField(max_length=100)

    def __str__(self):
        return self.user.username


class Parent(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    children = models.ManyToManyField('self', null=True, blank=True, related_name='c', symmetrical=False)

    def __str__(self):
        return self.user.username


class Child(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    parents = models.ManyToManyField('self', null=True, blank=True, related_name='p', symmetrical=False)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name_plural = "Children"


class Coach(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name_plural = "Coaches"
