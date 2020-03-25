import datetime

from django.utils.translation import gettext as _
from django.db import models

from polymorphic.models import PolymorphicModel
from polymorphic.showfields import ShowFieldType

from core.choices import CategoryNameChoices, EventTypeChoices, SkiTypeChoices
from family.models import Child
from users.models import User


class Season(models.Model):
    # format:   YYYY/YYYY
    # example:  2019/2020
    year = models.CharField(max_length=9, unique=True, primary_key=True)

    # # first day of skiing in the season
    start_date = models.DateTimeField(null=True, blank=True)
    # # last day of skiing in the season
    end_date = models.DateTimeField(null=True, blank=True)
    current = models.BooleanField(default=False)

    def __str__(self):
        return self.year


class Category(models.Model):
    # name
    season = models.ForeignKey(Season, on_delete=models.CASCADE)
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
        return "%s | %s" % (self.name, self.season)

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['id']
        unique_together = (('season', 'name'),)


# RES: https://django-polymorphic.readthedocs.io/en/stable/
class Event(ShowFieldType, PolymorphicModel):
    # RES (null vs blank): https://stackoverflow.com/questions/8609192/differentiate-null-true-blank-true-in-django
    season = models.ForeignKey(Season, on_delete=models.CASCADE, blank=True)
    category = models.ManyToManyField(Category)

    # It should be from category of the event: but it happened sometime that child which should't be on the training
    # because of his category came
    participants = models.ManyToManyField(Child, blank=True)

    # FIXME Validation -> event must have SkiTraining table if is type SKI_TRAINING, SKi_RACE and so on..
    type = models.CharField(
        max_length=50,
        choices=EventTypeChoices.choices
    )

    title = models.CharField(max_length=100, default="Default Title For Event")
    canceled = models.BooleanField(default=False)
    start_date = models.DateTimeField()

    # TODO in serializers default datetime + 1h from start
    end_date = models.DateTimeField(blank=True)

    location = models.CharField(max_length=50, blank=True)
    additional_info = models.CharField(max_length=150, blank=True)

    @property
    def get_type(self):
        return "test"

    def __str__(self):
        return "%s - %s" % (self.type, self.season)


class SkiEvent(Event):
    skis_type = models.CharField(
        max_length=3,
        choices=SkiTypeChoices.choices,
        default=SkiTypeChoices.ALL
    )

    # IDEA
    weather = models.CharField(max_length=100, blank=True, null=True)
    temperature = models.IntegerField(null=True, blank=True)
    snow_temperature = models.IntegerField(null=True, blank=True)

    class Meta:
        abstract = True


class SkiTraining(SkiEvent):
    gates = models.CharField(max_length=50, blank=True, null=True)
    number_of_runs = models.CharField(max_length=50, blank=True, null=True)

    # Slovan/Leitner/Poludňák
    ski_slope = models.CharField(max_length=50, blank=True, null=True)

    extra_field_for_ski_training = models.CharField(max_length=50, blank=True, null=True)

    # RES: https://stackoverflow.com/questions/4904230/django-change-default-value-for-an-extended-model-class
    # FIXME Validation -> SkiTraining could be only type EventTypeChoices.SKI_TRAINING -> return error if try to override
    def __init__(self, *args, **kwargs):
        self._meta.get_field('type').default = EventTypeChoices.SKI_TRAINING
        super(SkiEvent, self).__init__(*args, **kwargs)
        # !ATTENTION! -> This rewrite type everytime !!!
        self.type = EventTypeChoices.SKI_TRAINING


# IDEA: Future implementation
class SkiRace(SkiEvent):
    # results = models.OneToOneField(Results)
    # run = models.OneToOneField(Event)
    hotel_price = models.CharField(max_length=50, blank=True, null=True)
    book_hotel_from = models.DateTimeField(blank=True, null=True)
    book_hotel_to = models.DateTimeField(blank=True, null=True)

    def __init__(self, *args, **kwargs):
        self._meta.get_field('type').default = EventTypeChoices.SKI_RACE
        super(SkiEvent, self).__init__(*args, **kwargs)
        self.type = EventTypeChoices.SKI_RACE

# class AthleticTest(Event):
#     data= models.OneToOneField(TestsData)
#     results = models.OneToOneField(Results)
#     hotel_price = models.CharField(max_length=50, blank=True, null=True)
#     book_hotel_from = models.DateTimeField(blank=True, null=True)
#     book_hotel_to = models.DateTimeField(blank=True, null=True)
