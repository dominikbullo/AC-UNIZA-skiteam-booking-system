from django.contrib.auth import get_user_model
from django.core.mail import send_mail


def custom_create_user(**params):
    return get_user_model().objects.create_user(**params)


def send_custom_mail(new, old=None):
    print(old)
    print(new)

    if old:
        send_mail(subject='Subject',
                  message='Here is the message.',
                  from_email="from@example.com",
                  recipient_list=['to@example.com'],
                  fail_silently=False,
                  auth_user=None,
                  auth_password=None,
                  connection=None,
                  html_message=None)
