from allauth.account.models import EmailAddress
from allauth.account.signals import email_confirmed
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

from rest_framework.authtoken.models import Token

from events.models import Season
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


# @receiver(post_save, sender=settings.AUTH_USER_MODEL)
# def create_profile(sender, instance, created, **kwargs):
#     if created:
#         print("Creating profile: ", created)
#         Profile.objects.get_or_create(user=instance)
#         instance.save()

# making default_number True unique
# @receiver(post_save, sender=Season)
# def unique_current_season(sender, instance, **kwargs):
#     if instance.current:
#         Season.objects.all().exclude(pk=instance.pk).update(current=False)


@receiver(email_confirmed)
def update_user_email(sender, request, email_address, **kwargs):
    # Once the email address is confirmed, make new email_address primary.
    # This also sets user.email to the new email address.
    # email_address is an instance of allauth.account.models.EmailAddress
    email_address.set_as_primary()
    # Get rid of old email addresses
    stale_addresses = EmailAddress.objects.filter(
        user=email_address.user).exclude(primary=True).delete()


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def generate_token(sender, instance, created, **kwargs):
    if created:
        Token.objects.create(user=instance)
