# Generated by Django 3.1.2 on 2020-10-27 21:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0005_auto_20201027_2212'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='event',
            name='end_recur',
        ),
        migrations.RemoveField(
            model_name='event',
            name='group_id',
        ),
        migrations.RemoveField(
            model_name='event',
            name='start_recur',
        ),
        migrations.AddField(
            model_name='event',
            name='is_recur',
            field=models.BooleanField(default=False),
        ),
    ]
