import random
import string

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
