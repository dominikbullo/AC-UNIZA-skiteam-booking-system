from django.contrib.auth import get_user_model
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string


def custom_create_user(**params):
    return get_user_model().objects.create_user(**params)


def send_custom_mail(new_event, old_event=None):
    context = {
        'event': new_event
    }

    # render email text
    email_html_message = render_to_string('email/event_canceled.html', context)
    email_plaintext_message = "plain"

    # TODO Allow users to "unfollow", but for now it's ok
    emails = []
    for user in get_user_model().objects.all():
        email = user.email
        if email:
            emails.append(email)

    print("sending emails to ", emails)
    msg = EmailMultiAlternatives(
        # title:
        "Password Reset for {title}".format(title="Some website title"),
        # message:
        email_plaintext_message,
        # from:
        "noreply@somehost.local",
        # to:
        emails
    )
    msg.attach_alternative(email_html_message, "text/html")
    msg.send()
