import unicodedata

from config import settings
from django.contrib.auth import get_user_model
from django.core.mail import EmailMultiAlternatives, send_mail
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from sportagenda.apps.family.models import FamilyMember
from sportagenda.apps.users.models import User


def custom_create_user(**params):
    return get_user_model().objects.create_user(**params)


def send_custom_mail(new_event, template_file, old_event=None):
    context = {"event": new_event, "old_event": old_event}

    # render email text
    email_html_message = render_to_string(f"email/event/{template_file}.html", context)
    email_plaintext_message = render_to_string(
        f"email/event/{template_file}.txt", context
    )

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
        emails,
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


def generate_custom_unique_username(user_data):
    username = str(
        user_data.get("first_name", "") + user_data.get("last_name", "")
    ).lower()
    # RES: https://www.py.cz/Cestina3X
    username_candidate_normalized = ""
    for c in username:
        if not unicodedata.combining(c):
            username_candidate_normalized += c

    print(username_candidate_normalized)
    counter = 1
    while User.objects.filter(username=username):
        username = username + str(counter)
        counter += 1
    # RES: https://stackoverflow.com/questions/16664874/how-to-add-an-element-to-the-beginning-of-an-ordereddict
    user_data.update({"username": username})
