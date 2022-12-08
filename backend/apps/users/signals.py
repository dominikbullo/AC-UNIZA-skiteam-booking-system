from allauth.account.models import EmailAddress
from allauth.account.signals import email_confirmed
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.db import transaction
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.template.loader import render_to_string
from django_rest_passwordreset.signals import reset_password_token_created
from rest_framework.authtoken.models import Token

from apps.events.models import Event, Season
from core.utils import send_custom_mail


def notify_users(sender, instance, **kwargs):
    # If is forced to send email
    if instance.send_email:
        send_custom_mail(instance, "event_info")
        return

    try:
        # FIXME: https://stackoverflow.com/questions/25451087/django-select-for-update-cannot-be-used-outside-of-a-transaction
        with transaction.atomic():
            old = sender.objects.select_for_update().get(pk=instance.pk)
    except sender.DoesNotExist:
        pass  # Object is new
    else:
        # If event was canceled
        if not old.canceled and instance.canceled:
            send_custom_mail(instance, "event_canceled")
            return

        # If event was canceled but is live again
        if old.canceled and not instance.canceled:
            send_custom_mail(instance, "event_recreated", old)
            return


def pre_save_for_all_subclasses(model_class):
    pre_save.connect(notify_users, model_class)
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
    EmailAddress.objects.filter(user=email_address.user).exclude(primary=True).delete()


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def generate_token(sender, instance, created, **kwargs):
    if created:
        Token.objects.create(user=instance)


@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):
    """
    Handles password reset tokens
    When a token is created, an e-mail needs to be sent to the user
    :param sender: View Class that sent the signal
    :param instance: View Instance that sent the signal
    :param reset_password_token: Token Model Object
    :param args:
    :param kwargs:
    :return:
    """
    # send an e-mail to the user
    context = {
        "current_user": reset_password_token.user,
        "username": reset_password_token.user.username,
        "email": reset_password_token.user.email,
        "domain": instance.request.get_host(),
        "reset_password_url": "{}/reset-password/{}".format(
            # TODO: Test this url on production
            instance.request.get_host(),
            reset_password_token.key,
        ),
    }

    # render email text
    email_html_message = render_to_string("email/user/user_reset_password.html", context)
    email_plaintext_message = render_to_string("email/user/user_reset_password.txt", context)

    msg = EmailMultiAlternatives(
        # title:
        "Password Reset for {title}".format(title="SportAgenda"),
        # message:
        email_plaintext_message,
        # from:
        settings.DEFAULT_FROM_EMAIL,
        # to:
        [reset_password_token.user.email],
    )
    msg.attach_alternative(email_html_message, "text/html")
    msg.send()
