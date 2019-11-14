from django.db.models.signals import post_save
from django.dispatch import receiver

from users.models import User, Profile


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    # print("Created: ", created)
    if created:
        Profile.objects.create(user=instance)
