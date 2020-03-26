from django.db import models

from users.models import User


# RESOURCES
# https://www.youtube.com/watch?v=gf2-J9YOMcc&t=458s
# https://stackoverflow.com/questions/55006095/how-to-represent-a-family-relationship-in-django-using-manytomany-and-inlineform
# https://riptutorial.com/Download/django-rest-framework.pdf


class Family(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Families"
        ordering = ['id']


class FamilyMember(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    family = models.ForeignKey(Family, on_delete=models.CASCADE, related_name="members")
    extra_field_family_member = models.CharField(max_length=30, blank=True)

    def __str__(self):
        return self.user.display_name

    class Meta:
        ordering = ['user__date_joined']


class Child(FamilyMember):
    # RES (Many to many birectional): https://stackoverflow.com/questions/4881578/django-bi-directional-manytomany-how-to-prevent-table-creation-on-second-model
    categories = models.ManyToManyField('events.Category', blank=True)
    events = models.ManyToManyField('events.Event', blank=True)
    test_field = models.CharField(max_length=30, blank=True)

    def __str__(self):
        return self.user.display_name

    class Meta:
        verbose_name_plural = "Children"
