# Generated by Django 3.1.2 on 2020-10-28 18:27

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0012_eventtype_average_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='eventtype',
            name='average_time',
            field=models.DurationField(default=datetime.timedelta(seconds=3600)),
        ),
    ]
