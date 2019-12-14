from django.conf import settings
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from rest_framework.authtoken.models import Token

from users.models import Profile, User


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_profile(sender, instance, created, **kwargs):
    # print("Created: ", created)
    if created:
        # Create profile for every user
        Profile.objects.create(user=instance)

        # RES: https://www.django-rest-framework.org/api-guide/authentication/
        # Generate token for every user
        Token.objects.get_or_create(user=instance)


@receiver(pre_save, sender=settings.AUTH_USER_MODEL)
def update_username_from_email(sender, instance, **kwargs):
    user_email = instance.email
    try:
        username = user_email.split("@")[0]
    except Exception:
        print("@ not exist in username. Using first 30 chars of email")
        username = user_email

    # Limit o Django for username is 30 chars
    username = username[:30]
    n = 1
    while User.objects.exclude(pk=instance.pk).filter(username=username).exists():
        n += 1
        username = username[:(29 - len(str(n)))] + '-' + str(n)
    instance.username = username
