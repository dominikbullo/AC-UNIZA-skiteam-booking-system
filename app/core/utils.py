import random
import string
from django.contrib.auth import get_user_model

ALPHANUMERIC_CHARS = string.ascii_lowercase + string.digits
STRING_LENGTH = 6


def generate_random_string(chars=ALPHANUMERIC_CHARS, length=STRING_LENGTH):
    return "".join(random.choice(chars) for _ in range(length))


USER_TYPE_CHOICES = (
    (0, "Unidentified"),
    (1, 'Child'),
    (2, 'Parent'),
    (3, 'Coach'),
    (4, 'Admin'),
)
FAMILY_RELATION_CHOICE = (
    (1, 'Partner'),
    (2, 'Parent'),
    (3, 'Child'),
    (4, 'Sibling'),
)


def create_user(**params):
    # TODO create user with same method as in login
    return get_user_model().objects.create_user(**params)


def update_username_from_email_for_testing(email, **kwargs):
    user_email = email
    try:
        username = user_email.split("@")[0]
    except Exception:
        print("@ not exist in username. Using first 30 chars of email")
        username = user_email

    # Limit o Django for username is 30 chars
    username = username[:30]
    n = 1
    while get_user_model().objects.filter(username=username).exists():
        n += 1
        username = username[:(29 - len(str(n)))] + '-' + str(n)
    return username
