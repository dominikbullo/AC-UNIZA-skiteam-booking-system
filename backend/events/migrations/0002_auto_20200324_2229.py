# Generated by Django 3.0.4 on 2020-03-24 21:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='season',
            name='current',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='season',
            name='end',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='season',
            name='start',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]