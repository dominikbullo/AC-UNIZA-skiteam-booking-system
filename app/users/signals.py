from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

from rest_framework.authtoken.models import Token

from users.models import Profile


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_profile(sender, instance, created, **kwargs):
    # print("Created: ", created)
    if created:
        # Create profile for every user
        Profile.objects.create(user=instance)

        # RES: https://www.django-rest-framework.org/api-guide/authentication/
        # Generate token for every user
        Token.objects.get_or_create(user=instance)
