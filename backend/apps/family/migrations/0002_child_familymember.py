# Generated by Django 3.1.2 on 2020-10-27 20:14

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("users", "0001_initial"),
        ("events", "0001_initial"),
        ("family", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="FamilyMember",
            fields=[
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        primary_key=True,
                        serialize=False,
                        to="users.user",
                    ),
                ),
                (
                    "extra_field_family_member",
                    models.CharField(blank=True, max_length=30),
                ),
                (
                    "family",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="members",
                        to="family.family",
                    ),
                ),
            ],
            options={
                "ordering": ["user__date_joined"],
            },
        ),
        migrations.CreateModel(
            name="Child",
            fields=[
                (
                    "familymember_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="family.familymember",
                    ),
                ),
                ("test_field", models.CharField(blank=True, max_length=30)),
                (
                    "categories",
                    models.ManyToManyField(blank=True, to="events.Category"),
                ),
            ],
            options={
                "verbose_name_plural": "Children",
            },
            bases=("family.familymember",),
        ),
    ]