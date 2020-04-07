from django.db import models

from polymorphic.models import PolymorphicModel

from core.choices import CategoryNameChoices, EventTypeChoices, SkiTypeChoices
from family.models import Child
from users.models import Profile


class Season(models.Model):
    # format:   YYYY_YYYY
    # example:  2019_2020
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

    # year from to know who add into this cat
    year_from = models.DateField()

    # year until to know who add into this cat
    year_until = models.DateField()

    def __str__(self):
        return "%s | %s" % (self.name, self.season)

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
        return "%s - %s" % (self.name, self.ski_slope)

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

    start_date = models.DateTimeField()
    # TODO in serializers default datetime + 1h from start
    end_date = models.DateTimeField(blank=True)

    additional_info = models.CharField(max_length=150, blank=True)

    @property
    def get_type(self):
        return "test"

    def __str__(self):
        return "%s - %s" % (self.type, self.season)

        # # def save(self, *args, **kwargs):
        # #     # TODO FIX Type
        # #     # TODO if canceled or if is there some change in fields
        # #     # TODO compare if something change
        #
        # if self.id:
        #     old_event = Event.objects.get(pk=self.id)
        #     if not old_event.canceled and self.canceled:
        #         print("send_email() because event has been canceled")
        #
        #     if self.send_email:
        #         print("send_email() because it's true")
        #
        # super(Event, self).save()


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
