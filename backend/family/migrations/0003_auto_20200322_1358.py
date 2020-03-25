# Generated by Django 3.0.4 on 2020-03-22 12:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('family', '0002_child_familymember'),
    ]

    operations = [
        migrations.AlterField(
            model_name='familymember',
            name='family',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='members', to='family.Family'),
        ),
    ]