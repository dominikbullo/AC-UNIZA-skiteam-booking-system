from django.contrib.auth import get_user_model
from django.core.mail import send_mail, EmailMultiAlternatives
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string

from apps.family.models import FamilyMember
from config import settings


def custom_create_user(**params):
    return get_user_model().objects.create_user(**params)


def send_custom_mail(new_event, template_file, old_event=None):
    context = {
        'event'    : new_event,
        "old_event": old_event
    }

    # render email text
    email_html_message = render_to_string(f'email/event/{template_file}.html', context)
    email_plaintext_message = render_to_string(f'email/event/{template_file}.txt', context)

    emails = getEmailList()
    print("sending emails to ", emails)

    msg = EmailMultiAlternatives(
        # title:
        "Event update from SportAgenda",
        # message:
        email_plaintext_message,
        # from:
        settings.EMAIL_HOST_USER,
        # to:
        emails
    )

    msg.attach_alternative(email_html_message, "text/html")
    msg.send(fail_silently=True)


def getEmailList():
    # TODO Allow users to "unfollow", but for now it's ok
    emails = []
    # Alternative EmailAddress.objects.all()
    for user in get_user_model().objects.all():
        email = user.email
        if email:
            emails.append(email)
    return emails


def get_family_id(self, instance):
    try:
        return get_object_or_404(FamilyMember, user=instance.user).family_id
    except Exception as e:
        # FIXME: Cannot find family ID, cannot show /api/profile/ -> list
        #             #  probably it should be like events -> polymorphic
        print(e)
        print("User does not have family or is not family member!")
        return -1
