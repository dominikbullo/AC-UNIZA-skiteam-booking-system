# Generated by Django 3.1.2 on 2020-10-28 14:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0010_auto_20201027_2326'),
    ]

    operations = [
        migrations.RenameField(
            model_name='eventtype',
            old_name='type',
            new_name='name',
        ),
        migrations.AlterUniqueTogether(
            name='eventtype',
            unique_together={('name', 'need_skis')},
        ),
    ]
