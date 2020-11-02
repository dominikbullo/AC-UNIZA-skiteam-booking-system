import datetime

from django.db import models
from django.utils.translation import gettext as _

import sys, inspect

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
    TRAINING = 'TRAINING', _('Training')
    RACE = 'RACE', _('Race')
    CAMP = 'CAMP', _('Camp')
    VIDEO_ANALYZE = 'VIDEO_ANALYZE', _('Video Analyze')
    MEETING = 'MEETING', _('Meeting')


class SkiTypeChoices(models.TextChoices):
    SLALOM = 'SL', _('Slalom')
    GIANT_SLALOM = 'GS', _('Giant Slalom')
    SUPER_GIANT_SLALOM = 'SG', _('Super Giant Slalom')


class GenderChoices(models.TextChoices):
    MALE = 'M', _('Male')
    FEMALE = 'F', _('Female')


class FamilyRelationChoices(models.TextChoices):
    PARENT = 'PARENT', _('Parent')
    CHILD = 'CHILD', _('Child')
    SIBLING = 'SIBLING', _('Sibling')
    PARTNER = 'PARTNER', _('Partner')


def get_all_classes():
    ret = []
    for name, obj in inspect.getmembers(sys.modules[__name__]):
        if inspect.isclass(obj):
            ret.append(obj)
    return ret


def get_all_choices():
    classes = {
        SkiTypeChoices
    }
    # classes = get_all_classes()

    ret = {}
    # FIXME not return class name but some class attribute
    for item in classes:
        choices = []
        for choice, value in item.choices:
            choices.append({
                "key"        : choice,
                "displayName": value,
            })

        ret.update({item.__name__: choices})
    return ret
