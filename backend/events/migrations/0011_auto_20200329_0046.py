# Generated by Django 3.0.4 on 2020-03-28 23:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0009_auto_20200329_0033'),
        ('events', '0010_auto_20200329_0033'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='participants',
            field=models.ManyToManyField(blank=True, to='users.Profile'),
        ),
    ]
