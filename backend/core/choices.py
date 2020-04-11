import datetime

from django.db import models
from django.utils.translation import gettext as _

YEAR_CHOICES = [(r, r) for r in range(1984, datetime.date.today().year + 1)]


def year_choices():
    return [(r, r) for r in range(1984, datetime.date.today().year + 1)]


def current_year():
    return datetime.date.today().year


# RES: https://docs.djangoproject.com/en/dev/ref/models/fields/#django.db.models.Field.choices
class UserTypeChoices(models.TextChoices):
    PUBLIC = 'public', _('Public')
    CHILD = 'child', _('Child')
    PARENT = 'parent', _('Parent')
    COACH = 'coach', _('Coach')
    EDITOR = 'editor', _('Editor')
    ADMIN = 'admin', _('Admin')


class CategoryNameChoices(models.TextChoices):
    U_8 = 'U8', _('Superbaby')
    U_10 = 'U10', _('Mladší predžiaci')
    U_12 = 'U12', _('Starší predžiaci')
    U_14 = 'U14', _('Mladší žiaci')
    U_16 = 'U16', _('Starší žiaci')
    U_18 = 'U18', _('Juniory')
    U_21 = 'U21', _('Dospelý')


class EventTypeChoices(models.TextChoices):
    # FIXME Validation -> event must have SkiTraining table if is type SKI_TRAINING
    SKI_TRAINING = 'SKI_TRAINING', _('Ski Training')
    ATHLETIC_TRAINING = 'ATHLETIC_TRAINING', _('Athletic Training')
    SKI_RACE = 'SKI_RACE', _('Ski Race')
    SKI_CAMP = 'SKI_CAMP', _('Ski Camp')
    VIDEO_ANALYZE = 'VIDEO_ANALYZE', _('Video Analyze')
    MEETING = 'MEETING', _('Meeting')


class SkiTypeChoices(models.TextChoices):
    GIANT_SLALOM = 'GS', _('Giant Slalom')
    SLALOM = 'SL', _('Slalom')
    ALL = 'ALL', _('All')


class GenderChoices(models.TextChoices):
    MALE = 'M', _('Male')
    FEMALE = 'F', _('Female')


class FamilyRelationChoices(models.TextChoices):
    PARENT = 'PARENT', _('Parent')
    CHILD = 'CHILD', _('Child')
    SIBLING = 'SIBLING', _('Sibling')
    PARTNER = 'PARTNER', _('Partner')
