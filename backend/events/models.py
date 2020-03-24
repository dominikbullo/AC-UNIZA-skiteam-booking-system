import datetime

from django.utils.translation import gettext as _
from django.db import models
from polymorphic.models import PolymorphicModel

from core.choices import CategoryNameChoices, EventTypeChoices
from family.models import Child
from users.models import User


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
    # name
    session = models.ForeignKey(Season, on_delete=models.CASCADE)
    members = models.ManyToManyField(Child, blank=True)

    name = models.CharField(
        max_length=3,
        choices=CategoryNameChoices.choices,
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


# FIXME Validation -> event must have SkiTraining table if is type SKI_TRAINING
class Event(PolymorphicModel):
    # RES (null vs blank): https://stackoverflow.com/questions/8609192/differentiate-null-true-blank-true-in-django
    session = models.ForeignKey(Season, on_delete=models.CASCADE)
    category = models.ManyToManyField(Category)

    # It should be from category of the event: but it happened sometime that child which should't be on the training
    # because of his category came
    participants = models.ManyToManyField(Child, blank=True)

    type = models.CharField(
        max_length=50,
        choices=EventTypeChoices.choices
    )

    name = models.CharField(max_length=100, blank=True)
    start = models.DateTimeField()
    end = models.DateTimeField(null=True, blank=True)
    location = models.CharField(max_length=50, blank=True)
    additional_info = models.CharField(max_length=150, blank=True)

    def __str__(self):
        return "%s - %s" % (self.type, self.session)

    def __init__(self, *args, **kwargs):
        self._meta.get_field('type').editable = True
        super(Event, self).__init__(*args, **kwargs)
    # class Meta:
    #     abstract = True
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


class SkiTraining(SkiEvent):
    number_of_turns = models.PositiveSmallIntegerField(blank=True, null=True)
    extra_field_for_ski_training = models.CharField(max_length=50, blank=True, null=True)
    extra_field_for_ski_training1 = models.CharField(max_length=50, blank=True, null=True)
    extra_field_for_ski_training2 = models.CharField(max_length=50, blank=True, null=True)
    extra_field_for_ski_training3 = models.CharField(max_length=50, blank=True, null=True)

    # RES: https://stackoverflow.com/questions/4904230/django-change-default-value-for-an-extended-model-class
    # FIXME Validation -> SkiTraining could be only type EventTypeChoices.SKI_TRAINING -> return error if try to override
    def __init__(self, *args, **kwargs):
        self._meta.get_field('type').default = EventTypeChoices.SKI_TRAINING
        super(SkiEvent, self).__init__(*args, **kwargs)
        # !ATTENTION! -> This rewrite type everytime !!!
        self.type = EventTypeChoices.SKI_TRAINING
