# TODO this types
USER_TYPE_CHOICES = (
    (0, "Unidentified"),
    (1, 'Child'),
    (2, 'Parent'),
    (3, 'Coach'),
    (4, 'Admin'),
)

USER_TYPE_CHOICES_NEW_TEST = (
    ("unidentified", "Unidentified"),
    ("child", 'Child'),
    ("parent", 'Parent'),
    ("coach", 'Coach'),
    ("editor", 'Editor'),
    ("admin", 'Admin'),
)

GENDER_CHOICES = (
    ('M', 'Male'),
    ('F', 'Female'),
)

FAMILY_RELATION_CHOICE = (
    (1, 'Partner'),
    (2, 'Parent'),
    (3, 'Child'),
    (4, 'Sibling'),
)


def custom_create_user(**params):
    # TODO create user with same method as in login
    return get_user_model().objects.create_user(**params)
