# Generated by Django 3.1.3 on 2020-11-04 15:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("events", "0016_auto_20201104_1504"),
    ]

    operations = [
        migrations.AddField(
            model_name="accommodation",
            name="price",
            field=models.FloatField(blank=True, null=True),
        ),
    ]