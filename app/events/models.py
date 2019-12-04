from django.db import models


class Season(models.Model):
    # year
    # start date
    # end date
    pass


class Event(models.Model):
    # TODO should i create new table for every training or could i just add "type"
    # name
    # start
    # end
    # place
    # type
    # skis_type
    # canceled

    class Meta:
        abstract = True


class Category(models.Model):
    # name
    # year from season
    # year from to know who add into this cat
    # year until to know who add into this cat
    pass
