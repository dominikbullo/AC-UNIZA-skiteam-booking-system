from datetime import timedelta

from colorfield.fields import ColorField

from django.contrib.postgres.fields import ArrayField
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

    year_from = models.IntegerField(_('Year from'), choices=year_choices(), default=current_year() - 2)
    year_until = models.IntegerField(_('Year until'), choices=year_choices(), default=current_year())

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
    detail = models.CharField(max_length=50, blank=True, null=True)
    additional_info = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.display_name

    @property
    def display_name(self):
        if self.detail and self.detail != "":
            return "%s - %s" % (self.name, self.detail)
        return self.name

    class Meta:
        unique_together = (('name', 'detail'),)


class EventType(models.Model):
    name = models.CharField(
        max_length=50,
        choices=EventTypeChoices.choices
    )

    color = ColorField(default='#3788d8')
    text_color = ColorField(default="white")
    average_time = models.DurationField(default=timedelta(hours=1))

    need_skis = models.BooleanField(default=True)

    def __str__(self):
        if self.need_skis:
            return f"Ski {self.get_name_display()}"
        return f"{self.get_name_display()}"

    class Meta:
        unique_together = (('name', 'need_skis'),)


# RES: https://django-polymorphic.readthedocs.io/en/stable/
class Event(PolymorphicModel):
    # RES (null vs blank): https://stackoverflow.com/questions/8609192/differentiate-null-true-blank-true-in-django
    season = models.ForeignKey(Season, on_delete=models.CASCADE)
    type = models.ForeignKey(EventType, on_delete=models.DO_NOTHING)

    # IDEA: ONE training, more location (ski slope) e.g. Slovan žiaci, Leitner Predžiaci
    location = models.ForeignKey(Location, on_delete=models.DO_NOTHING)
    category = models.ManyToManyField(Category)

    participants = models.ManyToManyField('users.Profile', through=Profile.events.through, blank=True)

    canceled = models.BooleanField(default=False)
    send_email = models.BooleanField(default=False)

    start = models.DateTimeField()
    # TODO in serializers default datetime + 1h from start
    end = models.DateTimeField(blank=True)

    # recurring events
    is_recur = models.BooleanField(default=False)
    # group_id = models.IntegerField(max_length=150, blank=True)
    days_of_week = ArrayField(models.IntegerField(null=True, blank=True), null=True, blank=True)

    additional_info = models.CharField(max_length=150, blank=True)

    def __str__(self):
        return f"{self.type} | {self.season}"


class SkisType(models.Model):
    name = models.CharField(
        max_length=3,
        unique=True,
        choices=SkiTypeChoices.choices,
        default=SkiTypeChoices.GIANT_SLALOM
    )

    def __str__(self):
        return f"{self.name}"


class SkiEvent(Event):
    # RES: https://stackoverflow.com/questions/22538563/django-reverse-accessors-for-foreign-keys-clashing
    skis_type = models.ManyToManyField(
        to=SkisType,
        related_name='%(class)s_skis_type',  # the name for that relation from the point of view of a skill
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

    def __init__(self, *args, **kwargs):
        query = {
            "name"     : EventTypeChoices.TRAINING,
            "need_skis": True
        }

        super(SkiEvent, self).__init__(*args, **kwargs)
        self.type, created = EventType.objects.get_or_create(**query)


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

    propositions_URL = models.URLField(max_length=200, blank=True, null=True)
    hotel_price = models.CharField(max_length=50, blank=True, null=True)
    book_hotel_from = models.DateTimeField(blank=True, null=True)
    book_hotel_to = models.DateTimeField(blank=True, null=True)

    def __init__(self, *args, **kwargs):
        query = {
            "name"     : EventTypeChoices.RACE,
            "need_skis": True
        }
        super(SkiEvent, self).__init__(*args, **kwargs)
        self.type, created = EventType.objects.get_or_create(**query)
