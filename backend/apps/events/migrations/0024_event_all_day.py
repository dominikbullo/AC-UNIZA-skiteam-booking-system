# Generated by Django 3.1.3 on 2020-11-18 16:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("events", "0023_auto_20201118_1740"),
    ]

    operations = [
        migrations.AddField(
            model_name="event",
            name="all_day",
            field=models.BooleanField(default=False),
        ),
    ]
