# Generated by Django 3.0.4 on 2020-03-25 16:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0004_auto_20200325_1635'),
    ]

    operations = [
        migrations.RenameField(
            model_name='event',
            old_name='end',
            new_name='end_date',
        ),
        migrations.RenameField(
            model_name='event',
            old_name='start',
            new_name='start_date',
        ),
        migrations.RenameField(
            model_name='season',
            old_name='end',
            new_name='end_date',
        ),
        migrations.RenameField(
            model_name='season',
            old_name='start',
            new_name='start_date',
        ),
    ]
