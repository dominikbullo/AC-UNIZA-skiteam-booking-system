# Generated by Django 3.0.4 on 2020-03-25 15:35

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('events', '0003_auto_20200325_1457'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='end',
            field=models.DateTimeField(blank=True, default='2011-03-03 15:15'),
            preserve_default=False,
        ),
    ]