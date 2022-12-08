from datetime import timedelta

from colorfield.fields import ColorField
from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.db.models import Q
from django.utils.translation import gettext as _
from polymorphic.models import PolymorphicModel
from simple_history.models import HistoricalRecords

from apps.family.models import Child
from apps.users.models import Profile
from core.choices import CategoryNameChoices, EventTypeChoices, SkiTypeChoices, current_year, year_choices


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
    members = models.ManyToManyField("family.Child", through=Child.categories.through, blank=True)

    name = models.CharField(
        max_length=3,
        choices=CategoryNameChoices.choices,
    )

    year_from = models.IntegerField(_("Year from"), choices=year_choices(), default=current_year() - 2)
    year_until = models.IntegerField(_("Year until"), choices=year_choices(), default=current_year())

    def __str__(self):
        return "{name} | {season}".format(name=self.name, season=self.season)

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ["-year_from", "id"]
        # One child, One category, One Season -> many categories in different seasons
        unique_together = (("season", "name"),)


class Location(models.Model):
    # RES: https://github.com/caioariede/django-location-field
    name = models.CharField(max_length=80)
    detail = models.CharField(max_length=50, blank=True, null=True)
    need_ski = models.BooleanField(default=True)
    additional_info = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.display_name

    @property
    def display_name(self):
        if self.detail and self.detail != "":
            return "%s - %s" % (self.name, self.detail)
        return self.name

    class Meta:
        unique_together = (("name", "detail"),)


class EventType(models.Model):
    type = models.CharField(max_length=50, choices=EventTypeChoices.choices)

    color = ColorField(default="#3788d8")
    text_color = ColorField(default="white")
    average_time = models.DurationField(default=timedelta(hours=1))

    need_skis = models.BooleanField(default=True)

    def __str__(self):
        return self.display_name

    @property
    def display_name(self):
        if self.need_skis:
            return f"Ski {self.get_type_display()}"
        return f"{self.get_type_display()}"

    class Meta:
        unique_together = (("type", "need_skis"),)


class Accommodation(models.Model):
    interest = models.BooleanField(default=False)

    start = models.DateField()
    end = models.DateField()

    adults = models.IntegerField(null=True, blank=True)
    children = models.IntegerField(null=True, blank=True)

    price = models.FloatField(null=True, blank=True)
    name = models.CharField(max_length=150, null=True)
    website = models.URLField(max_length=200, null=True)

    # TODO: status with choices
    # status = models.CharField(max_length=150)

    def __str__(self):
        return self.display_name

    @property
    def display_name(self):
        if self.name:
            return self.name
        return self.website

    class Meta:
        constraints = [
            models.CheckConstraint(
                check=Q(name__isnull=False) | Q(website__isnull=False),
                name="not_both_null",
            )
        ]


# RES: https://django-polymorphic.readthedocs.io/en/stable/
# RES (null vs blank): https://stackoverflow.com/questions/8609192/differentiate-null-true-blank-true-in-django
class Event(PolymorphicModel):
    created = models.DateTimeField(auto_now_add=True)
    season = models.ForeignKey(Season, on_delete=models.CASCADE)
    type = models.ForeignKey(EventType, on_delete=models.DO_NOTHING)

    accommodation = models.ManyToManyField(Accommodation, blank=True)

    # IDEA: ONE training, more location (ski slope) e.g. Slovan žiaci, Leitner Predžiaci
    location = models.ForeignKey(Location, on_delete=models.DO_NOTHING)
    category = models.ManyToManyField(Category)

    participants = models.ManyToManyField("users.Profile", through=Profile.events.through, blank=True)

    all_day = models.BooleanField(default=False)
    start = models.DateTimeField()
    end = models.DateTimeField(blank=True, null=True)

    # recurring events
    is_recur = models.BooleanField(default=False)
    # group_id = models.IntegerField(max_length=150, blank=True)
    days_of_week = ArrayField(models.IntegerField(null=True, blank=True), null=True, blank=True)

    canceled = models.BooleanField(default=False)
    send_email = models.BooleanField(default=False)

    additional_info = models.CharField(max_length=150, blank=True)

    def __str__(self):
        return f"{self.start.strftime('%d.%m.%Y %H:%M')} | {self.type}"

    def need_skis(self):
        return self.type.need_skis

    def has_accommodation(self):
        return self.accommodation is not None


class EventResponse(models.Model):
    event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE,
        blank=False,
        null=True,
        related_name="responses",
    )
    # answerer = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='answerers')
    user_to_event = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="users_to_event")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    history = HistoricalRecords()

    # Idea:  Reason why not
    # Yes/No -> if not found -> no answer
    going = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user_to_event}"


class SkisType(models.Model):
    name = models.CharField(
        max_length=3,
        unique=True,
        choices=SkiTypeChoices.choices,
        default=SkiTypeChoices.GIANT_SLALOM,
    )

    def __str__(self):
        return self.display_name

    @property
    def display_name(self):
        return f"{self.name}"


class SkiEvent(Event):
    # RES: https://stackoverflow.com/questions/22538563/django-reverse-accessors-for-foreign-keys-clashing
    skis_type = models.ManyToManyField(
        to=SkisType,
        related_name="%(class)s_skis_type",  # the name for that relation from the point of view of a skill
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
        query = {"type": EventTypeChoices.TRAINING, "need_skis": True}

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
        unique_together = (("name", "club"),)


class SkiRace(SkiEvent):
    organizer = models.ForeignKey(RaceOrganizer, on_delete=models.DO_NOTHING)

    propositions_URL = models.URLField(max_length=200, blank=True, null=True)
    hotel_price = models.CharField(max_length=50, blank=True, null=True)
    book_hotel_from = models.DateTimeField(blank=True, null=True)
    book_hotel_to = models.DateTimeField(blank=True, null=True)

    def __init__(self, *args, **kwargs):
        query = {"type": EventTypeChoices.RACE, "need_skis": True}
        super(SkiEvent, self).__init__(*args, **kwargs)
        self.type, created = EventType.objects.get_or_create(**query)
