# Generated by Django 3.1.3 on 2020-12-04 21:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('family', '0002_child_familymember'),
    ]

    operations = [
        migrations.AddField(
            model_name='family',
            name='token',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
