# Generated by Django 3.0.5 on 2020-04-04 08:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0004_auto_20200330_1957'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='season',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='events.Season'),
        ),
    ]
