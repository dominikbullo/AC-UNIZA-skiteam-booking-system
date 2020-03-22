# import datetime
#
# from django.utils.translation import gettext as _
# from django.db import models
#
#
# class Season(models.Model):
#     # format:   YYYY/YYYY
#     id = models.AutoField(primary_key=True)
#     # example:  2019/2020
#     year = models.CharField(max_length=9, unique=True)
#
#     # # first day of skiing in the session
#     # start = models.DateTimeField(blank=True)
#     # # last day of skiing in the session
#     # end = models.DateTimeField(blank=True)
#     def __str__(self):
#         return self.year
#
#
# class Category(models.Model):
#     id = models.AutoField(primary_key=True)
#
#     class Categories(models.TextChoices):
#         U_8 = 'U_8', _('Superbaby')
#         U_10 = 'U_10', _('Mladší predžiaci')
#         U_12 = 'U_12', _('Starší predžiaci')
#         U_14 = 'U_14', _('Mladší žiaci')
#         U_16 = 'U_16', _('Starší žiaci')
#         U_18 = 'U_18', _('Juniory')
#         U_21 = 'U_21', _('Dospelý')
#
#     # name
#     name = models.CharField(
#         max_length=4,
#         choices=Categories.choices,
#         default="Undefinied"
#     )
#
#     # year from season
#     # session = models.ForeignKey(Season, on_delete=models.CASCADE)
#     # session = models.CharField(max_length=100, blank=True)
#
#     # # year from to know who add into this cat
#     # year_from = models.DateField(blank=True)
#     # # year until to know who add into this cat
#     # year_until = models.DateField(blank=True)
#
#     def __str__(self):
#         return self.name
#
#     class Meta:
#         verbose_name_plural = "Categories"
#         ordering = ['id']
#
#
# class Event(models.Model):
#     id = models.AutoField(primary_key=True)
#     session = models.ForeignKey(Season, on_delete=models.CASCADE)
#     # # TODO config
#     # category = models.ManyToManyField(Category)
#
#     name = models.CharField(max_length=100, blank=True)
#     start = models.DateTimeField(default=datetime.datetime.now())
#     end = models.DateTimeField(blank=True, default=datetime.datetime.now())
#     location = models.CharField(max_length=50, blank=True)
#     additional_info = models.CharField(max_length=150, blank=True)
#
#     def __str__(self):
#         return self.name
#
#     class Meta:
#         abstract = True
#
#
# class SkiEvent(Event):
#     class SkiType(models.TextChoices):
#         GIANT_SLALOM = 'GS', _('Giant Slalom')
#         SLALOM = 'SL', _('Slalom')
#         ALL = 'AL', _('All')
#
#     skis_type = models.CharField(
#         max_length=2,
#         choices=SkiType.choices,
#         default=SkiType.ALL,
#     )
#
#     class Meta:
#         abstract = True
#
#
# class SkiTraining(SkiEvent):
#     class SkiType(models.TextChoices):
#         GIANT_SLALOM = 'GS', _('Giant Slalom')
#         SLALOM = 'SL', _('Slalom')
#         ALL = 'AL', _('All')
#
#     skis_type = models.CharField(
#         max_length=2,
#         choices=SkiType.choices,
#         default=SkiType.ALL,
#     )
#
#     number_of_turns = models.PositiveSmallIntegerField(blank=True)
#
#
# class SkiRace(SkiEvent):
#     pass
#
#
# class AthleticTraining(Event):
#     pass
#
#
# class AthleticCamp(Event):
#     pass
#
# # https://docs.djangoproject.com/en/3.0/ref/models/fields/
# # from django.utils.translation import gettext_lazy as _
# #
# #
# # class Student(models.Model):
# #     class YearInSchool(models.TextChoices):
# #         FRESHMAN = 'FR', _('Freshman')
# #         SOPHOMORE = 'SO', _('Sophomore')
# #         JUNIOR = 'JR', _('Junior')
# #         SENIOR = 'SR', _('Senior')
# #         GRADUATE = 'GR', _('Graduate')
# #
# #     year_in_school = models.CharField(
# #         max_length=2,
# #         choices=YearInSchool.choices,
# #         default=YearInSchool.FRESHMAN,
# #     )
# #
# #     def is_upperclass(self):
# #         return self.year_in_school in {YearInSchool.JUNIOR, YearInSchool.SENIOR}
