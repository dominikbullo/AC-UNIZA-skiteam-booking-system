from allauth.account.models import EmailAddress
from django.conf import settings
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from rest_framework.authtoken.models import Token

from users.models import Profile


# @receiver(pre_save, sender=settings.AUTH_USER_MODEL)
# def set_username(sender, instance, **kwargs):
#     if not instance.username:
#         username = instance.first_name
#         counter = 1
#         while get_user_model().objects.filter(username=username):
#             username = instance.first_name + str(counter)
#             counter += 1
#         instance.username = username


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_profile(sender, instance, created, **kwargs):
    if created:
        print("Creating profile: ", created)
        # # Create profile for every user
        Profile.objects.create(user=instance)


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def generate_token(sender, instance, created, **kwargs):
    if created:
        print("Generate token: ", created)
        Token.objects.create(user=instance)
