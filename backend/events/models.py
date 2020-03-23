import datetime

from django.utils.translation import gettext as _
from django.db import models

from family.models import Child


# RES: https://docs.djangoproject.com/en/dev/ref/models/fields/#django.db.models.Field.choices
class EventTypeChoices(models.TextChoices):
    SKI_TRAINING = 'Ski Training'
    SKI_RACE = 'SKi Race'
    SKI_CAMP = 'SKi Camp'


class Season(models.Model):
    # format:   YYYY/YYYY
    # example:  2019/2020
    year = models.CharField(max_length=9, unique=True, primary_key=True)

    # # first day of skiing in the session
    # start = models.DateTimeField(blank=True)
    # # last day of skiing in the session
    # end = models.DateTimeField(blank=True)
    def __str__(self):
        return self.year


class Category(models.Model):
    class Categories(models.TextChoices):
        U_8 = 'U8', _('Superbaby')
        U_10 = 'U10', _('Mladší predžiaci')
        U_12 = 'U12', _('Starší predžiaci')
        U_14 = 'U14', _('Mladší žiaci')
        U_16 = 'U16', _('Starší žiaci')
        U_18 = 'U18', _('Juniory')
        U_21 = 'U21', _('Dospelý')

    # name
    session = models.ForeignKey(Season, on_delete=models.CASCADE)
    children = models.ManyToManyField(Child, blank=True)

    name = models.CharField(
        max_length=3,
        choices=Categories.choices,
    )

    # year from to know who add into this cat
    year_from = models.DateField()

    # year until to know who add into this cat
    year_until = models.DateField()

    def __str__(self):
        return "%s | %s" % (self.name, self.session)

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['id']
        unique_together = (('session', 'name'),)


class Event(models.Model):
    # RES (null vs blank): https://stackoverflow.com/questions/8609192/differentiate-null-true-blank-true-in-django
    session = models.ForeignKey(Season, on_delete=models.CASCADE)
    category = models.ManyToManyField(Category)

    # It should be from category of the event: but it happened sometime that child which should't be on the training
    # because of his category came
    participants = models.ManyToManyField(Child, blank=True)

    type = models.CharField(
        max_length=50,
        choices=EventTypeChoices.choices,
        editable=True
    )

    name = models.CharField(max_length=100, blank=True)
    start = models.DateTimeField()
    end = models.DateTimeField(null=True, blank=True)
    location = models.CharField(max_length=50, blank=True)
    additional_info = models.CharField(max_length=150, blank=True)

    def __str__(self):
        return "%s - %s" % (self.type, self.session)

    # class Meta:
    #     unique_together = (('type', 'start'),)


class SkiEvent(Event):
    class SkiType(models.TextChoices):
        GIANT_SLALOM = 'GS', _('Giant Slalom')
        SLALOM = 'SL', _('Slalom')
        ALL = 'AL', _('All')

    skis_type = models.CharField(
        max_length=2,
        choices=SkiType.choices,
        default=SkiType.ALL,
    )

    class Meta:
        abstract = True


#
class SkiTraining(SkiEvent):
    number_of_turns = models.PositiveSmallIntegerField(blank=True, null=True)

    # # RES: https://stackoverflow.com/questions/4904230/django-change-default-value-for-an-extended-model-class
    def __init__(self, *args, **kwargs):
        self._meta.get_field('type').default = EventTypeChoices.SKI_TRAINING
        super(SkiEvent, self).__init__(*args, **kwargs)
        # !ATTENTION! -> This rewrite type everytime !!!
        self.type = EventTypeChoices.SKI_TRAINING

# RES: https://stackoverflow.com/questions/7884757/how-do-you-change-field-arguments-in-django-model-subclasses

# class SkiRace(SkiEvent):
#
#     def __init__(self, *args, **kwargs):
#         super(SkiEvent, self).__init__(*args, **kwargs)
#         self.ques_type = EventTypeChoices.SKI_TRAINING
#
# # RES: https://docs.djangoproject.com/en/3.0/ref/models/fields/
