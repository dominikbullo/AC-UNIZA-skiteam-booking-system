import datetime

from django.db import models
from django.utils.translation import gettext as _

from polymorphic.models import PolymorphicModel

from core.choices import CategoryNameChoices, EventTypeChoices, SkiTypeChoices, year_choices, current_year
from apps.family.models import Child
from apps.users.models import Profile


class Season(models.Model):
    # format:   YYYY-YYYY
    # example:  2019-2020
    year = models.CharField(max_length=9, unique=True)
    current = models.BooleanField(default=False)

    # first day of skiing in the season
    start_date = models.DateField(null=True, blank=True)
    # last day of skiing in the season
    end_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.year


class Category(models.Model):
    season = models.ForeignKey(Season, on_delete=models.CASCADE)
    # RES (Many to many birectional): https://stackoverflow.com/questions/4881578/django-bi-directional-manytomany-how-to-prevent-table-creation-on-second-model
    members = models.ManyToManyField('family.Child', through=Child.categories.through, blank=True)

    name = models.CharField(
        max_length=3,
        choices=CategoryNameChoices.choices,
    )

    # year_from = models.IntegerField(_('Year from'), choices=year_choices(), default=current_year() - 2)
    # year_until = models.IntegerField(_('Year until'), choices=year_choices(), default=current_year())

    def __str__(self):
        return "{name} | {season}".format(name=self.name, season=self.season)

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['id']
        # TODO -> cannot set unique_together with category members and season -> signals
        # One child, One category, One Season -> many categories in different seasons
        unique_together = (('season', 'name'),)


class Location(models.Model):
    # TODO RES: https://github.com/caioariede/django-location-field
    name = models.CharField(max_length=80)
    ski_slope = models.CharField(max_length=50, blank=True, null=True)
    additional_info = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.display_name

    @property
    def display_name(self):
        if self.ski_slope and self.ski_slope != "":
            return "%s - %s" % (self.name, self.ski_slope)
        return self.name

    class Meta:
        unique_together = (('name', 'ski_slope'),)


# RES: https://django-polymorphic.readthedocs.io/en/stable/
class Event(PolymorphicModel):
    # RES (null vs blank): https://stackoverflow.com/questions/8609192/differentiate-null-true-blank-true-in-django
    season = models.ForeignKey(Season, on_delete=models.CASCADE)

    # IDEA: ONE training, more location (ski slope) e.g. Slovan žiaci, Leitner Predžiaci
    location = models.ForeignKey(Location, on_delete=models.DO_NOTHING)
    category = models.ManyToManyField(Category)

    participants = models.ManyToManyField('users.Profile', through=Profile.events.through, blank=True)

    # FIXME Validation -> event must have SkiTraining table if is type SKI_TRAINING, SKi_RACE and so on..
    type = models.CharField(
        max_length=50,
        choices=EventTypeChoices.choices
    )

    canceled = models.BooleanField(default=False)
    send_email = models.BooleanField(default=False)

    start = models.DateTimeField()
    # TODO in serializers default datetime + 1h from start
    end = models.DateTimeField(blank=True)

    additional_info = models.CharField(max_length=150, blank=True)

    def __str__(self):
        return "{type} | {season}".format(type=self.get_type_display(), season=self.season)


class SkiEvent(Event):
    skis_type = models.CharField(
        max_length=3,
        choices=SkiTypeChoices.choices,
        default=SkiTypeChoices.ALL
    )

    # IDEA
    # weather = models.CharField(max_length=100, blank=True, null=True)
    # snow_temperature = models.IntegerField(null=True, blank=True)
    temperature = models.IntegerField(null=True, blank=True)

    class Meta:
        abstract = True


class SkiTraining(SkiEvent):
    gates = models.CharField(max_length=50, blank=True, null=True)
    number_of_runs = models.CharField(max_length=50, blank=True, null=True)

    # RES: https://stackoverflow.com/questions/4904230/django-change-default-value-for-an-extended-model-class
    # FIXME Validation -> SkiTraining could be only type EventTypeChoices.SKI_TRAINING -> return error if try to override
    def __init__(self, *args, **kwargs):
        self._meta.get_field('type').default = EventTypeChoices.SKI_TRAINING
        super(SkiEvent, self).__init__(*args, **kwargs)
        # !ATTENTION! -> This rewrite type everytime !!!
        self.type = EventTypeChoices.SKI_TRAINING


class RaceOrganizer(models.Model):
    # SLA/Public/ZSL
    name = models.CharField(max_length=50)
    shorthand = models.CharField(max_length=15)
    website = models.URLField(max_length=200, blank=True, null=True)
    club = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return self.display_name

    @property
    def display_name(self):
        if self.club and self.club != "":
            return "%s | %s" % (self.shorthand, self.club)
        return self.shorthand

    def clean(self):
        """
        Checks that we do not create multiple categories with
        no parent and the same name.
        """
        from django.core.exceptions import ValidationError
        if self.club is None and RaceOrganizer.objects.filter(name=self.name, club=None).exists():
            raise ValidationError("Another RaceOrganizer with name %s and no club already exists" % self.name)

    class Meta:
        unique_together = (('name', 'club'),)


class SkiRace(SkiEvent):
    organizer = models.ForeignKey(RaceOrganizer, on_delete=models.DO_NOTHING)
    # results = models.OneToOneField(Results)

    propositionURL = models.URLField(max_length=200, blank=True, null=True)
    hotel_price = models.CharField(max_length=50, blank=True, null=True)
    book_hotel_from = models.DateTimeField(blank=True, null=True)
    book_hotel_to = models.DateTimeField(blank=True, null=True)

    def __init__(self, *args, **kwargs):
        self._meta.get_field('type').default = EventTypeChoices.SKI_RACE
        super(SkiEvent, self).__init__(*args, **kwargs)
        self._meta.get_field('type').default = EventTypeChoices.SKI_RACE
        self.type = EventTypeChoices.SKI_RACE

# class AthleticTest(Event):
#     data= models.OneToOneField(TestsData)
#     results = models.OneToOneField(Results)
#     hotel_price = models.CharField(max_length=50, blank=True, null=True)
#     book_hotel_from = models.DateTimeField(blank=True, null=True)
#     book_hotel_to = models.DateTimeField(blank=True, null=True)
