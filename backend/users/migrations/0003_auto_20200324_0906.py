# Generated by Django 3.0.4 on 2020-03-24 08:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_auto_20200323_1055'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='user_role',
            field=models.PositiveSmallIntegerField(blank=True, choices=[('public', 'Public'), ('child', 'Child'), ('parent', 'Parent'), ('coach', 'Coach'), ('editor', 'Editor'), ('admin', 'Admin')], null=True),
        ),
    ]