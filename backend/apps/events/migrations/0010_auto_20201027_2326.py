# Generated by Django 3.1.2 on 2020-10-27 22:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("events", "0009_auto_20201027_2245"),
    ]

    operations = [
        migrations.RenameField(
            model_name="skirace",
            old_name="propositionURL",
            new_name="propositions_URL",
        ),
    ]
