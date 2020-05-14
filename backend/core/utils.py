from django.contrib.auth import get_user_model
from django.core.mail import send_mail


def custom_create_user(**params):
    return get_user_model().objects.create_user(**params)


def send_custom_mail(new, old=None):
    try:
        # print(old)
        # print(new)

        if old:
            send_mail(
                subject='Udalosť zmenená',
                message='Event was canceled',
                from_email="from@example.com",
                recipient_list=['to@example.com'],
                fail_silently=False,
                auth_user=None,
                auth_password=None,
                connection=None,
                html_message=None
            )
        else:
            send_mail(
                subject='Udalosť zmenená',
                message='Event is up again canceled',
                from_email="from@example.com",
                recipient_list=['to@example.com'],
                fail_silently=False,
                auth_user=None,
                auth_password=None,
                connection=None,
                html_message=None
            )

    except Exception as e:
        print(e)
