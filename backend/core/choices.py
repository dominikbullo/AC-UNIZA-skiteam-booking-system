from django.db import models
from django.utils.translation import gettext as _

USER_TYPE_CHOICES = (
    (0, "Public"),
    (1, 'Child'),
    (2, 'Parent'),
    (3, 'Coach'),
    (4, 'Admin'),
)


class CategoryNameChoices(models.TextChoices):
    U_8 = 'U8', _('Superbaby')
    U_10 = 'U10', _('Mladší predžiaci')
    U_12 = 'U12', _('Starší predžiaci')
    U_14 = 'U14', _('Mladší žiaci')
    U_16 = 'U16', _('Starší žiaci')
    U_18 = 'U18', _('Juniory')
    U_21 = 'U21', _('Dospelý')


class EventTypeChoices(models.TextChoices):
    SKI_TRAINING = 'SKI_TRAINING', _('Ski Training')
    SKI_RACE = 'SKI_RACE', _('Ski Race')
    SKI_CAMP = 'SKI_CAMP', _('Si Camp')


class UserTypeChoices(models.TextChoices):
    SKI_TRAINING = 'SKI_TRAINING', _('Ski Training')
    SKI_RACE = 'SKI_RACE', _('Ski Race')
    SKI_CAMP = 'SKI_CAMP', _('Si Camp')


USER_TYPE_CHOICES_NEW_TEST = (
    ("public", "Public"),
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


class FamilyRelationChoices(models.TextChoices):
    PARENT = 'PARENT', _('Parent')
    CHILD = 'CHILD', _('Child')
    SIBLING = 'SIBLING', _('Sibling')
    PARTNER = 'PARTNER', _('Partner')


FAMILY_RELATION_CHOICE = (
    (1, 'Partner'),
    (2, 'Parent'),
    (3, 'Child'),
    (4, 'Sibling'),
)
