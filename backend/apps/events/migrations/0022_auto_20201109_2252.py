# Generated by Django 3.1.3 on 2020-11-09 21:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0021_auto_20201106_2240'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='accommodation',
            field=models.ManyToManyField(blank=True, to='events.Accommodation'),
        ),
    ]
