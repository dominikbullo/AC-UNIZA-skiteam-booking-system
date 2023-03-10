# Generated by Django 3.1.2 on 2020-10-27 21:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0007_auto_20201027_2236'),
    ]

    operations = [
        migrations.AlterField(
            model_name='eventtype',
            name='type',
            field=models.CharField(choices=[('TRAINING', 'Training'), ('RACE', 'Race'), ('CAMP', 'Camp'), ('VIDEO_ANALYZE', 'Video Analyze'), ('MEETING', 'Meeting')], max_length=50),
        ),
        migrations.AlterUniqueTogether(
            name='eventtype',
            unique_together={('type', 'need_skis')},
        ),
    ]
