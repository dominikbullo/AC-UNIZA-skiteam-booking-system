# Generated by Django 3.0.4 on 2020-03-25 13:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0002_auto_20200324_2229'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='season',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='events.Season'),
        ),
        migrations.AlterField(
            model_name='skirace',
            name='skis_type',
            field=models.CharField(choices=[('GS', 'Giant Slalom'), ('SL', 'Slalom'), ('ALL', 'All')], default='ALL', max_length=3),
        ),
        migrations.AlterField(
            model_name='skitraining',
            name='skis_type',
            field=models.CharField(choices=[('GS', 'Giant Slalom'), ('SL', 'Slalom'), ('ALL', 'All')], default='ALL', max_length=3),
        ),
    ]