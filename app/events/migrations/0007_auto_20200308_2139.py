# Generated by Django 3.0.4 on 2020-03-08 21:39

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0006_auto_20200308_2110'),
    ]

    operations = [
        migrations.AlterField(
            model_name='athleticcamp',
            name='end',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2020, 3, 8, 21, 39, 28, 582477)),
        ),
        migrations.AlterField(
            model_name='athleticcamp',
            name='start',
            field=models.DateTimeField(default=datetime.datetime(2020, 3, 8, 21, 39, 28, 582457)),
        ),
        migrations.AlterField(
            model_name='athletictraining',
            name='end',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2020, 3, 8, 21, 39, 28, 582477)),
        ),
        migrations.AlterField(
            model_name='athletictraining',
            name='start',
            field=models.DateTimeField(default=datetime.datetime(2020, 3, 8, 21, 39, 28, 582457)),
        ),
        migrations.AlterField(
            model_name='skirace',
            name='end',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2020, 3, 8, 21, 39, 28, 582477)),
        ),
        migrations.AlterField(
            model_name='skirace',
            name='start',
            field=models.DateTimeField(default=datetime.datetime(2020, 3, 8, 21, 39, 28, 582457)),
        ),
        migrations.AlterField(
            model_name='skitraining',
            name='end',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2020, 3, 8, 21, 39, 28, 582477)),
        ),
        migrations.AlterField(
            model_name='skitraining',
            name='start',
            field=models.DateTimeField(default=datetime.datetime(2020, 3, 8, 21, 39, 28, 582457)),
        ),
    ]
