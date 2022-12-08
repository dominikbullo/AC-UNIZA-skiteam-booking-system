# Generated by Django 3.1.2 on 2020-10-27 21:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("events", "0006_auto_20201027_2218"),
    ]

    operations = [
        migrations.RenameField(
            model_name="location",
            old_name="ski_slope",
            new_name="detail",
        ),
        migrations.AlterUniqueTogether(
            name="location",
            unique_together={("name", "detail")},
        ),
    ]
