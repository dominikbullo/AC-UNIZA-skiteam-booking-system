from allauth.account.models import EmailAddress
from allauth.account.signals import email_confirmed

from django.conf import settings
from django.db import transaction
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from rest_framework.authtoken.models import Token

from events.models import Season, Event


def send_email_if_flag_enabled(sender, instance, **kwargs):
    if instance.send_email:
        print("Sending mails, because send email was check")
        instance.send_email = False


@transaction.atomic
def send_email_if_canceled_change(sender, instance, **kwargs):
    try:
        obj = sender.objects.select_for_update().get(pk=instance.pk)
    except sender.DoesNotExist:
        pass  # Object is new, so field hasn't technically changed, but you may want to do something else here.
    else:
        # If event was canceled
        if not obj.canceled and instance.canceled:
            print("send_email() because event has been canceled")
            return

        # If event was canceled but is live again
        if obj.canceled and not instance.canceled:
            print("send_email() because event has been canceled but is live again")
            return


def pre_save_for_all_subclasses(model_class):
    pre_save.connect(send_email_if_flag_enabled, model_class)
    pre_save.connect(send_email_if_canceled_change, model_class)
    if len(model_class.__subclasses__()) > 0:
        for subClass in model_class.__subclasses__():
            pre_save_for_all_subclasses(subClass)


pre_save_for_all_subclasses(Event)


# # TODO for profile data fill profile
# @receiver(post_save, sender=settings.AUTH_USER_MODEL)
# def create_profile(sender, instance, created, **kwargs):
#     if created:
#         print("Creating profile: ", created, "details: ", sender, instance)
#         Profile.objects.create(user=instance)
#         instance.save()


# making olny one season current
@receiver(post_save, sender=Season)
def unique_current_season(sender, instance, **kwargs):
    if instance.current:
        Season.objects.all().exclude(pk=instance.pk).update(current=False)


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
