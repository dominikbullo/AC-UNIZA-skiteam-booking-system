# Generated by Django 2.2.7 on 2019-11-14 10:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_auto_20191114_1129'),
    ]

    operations = [
        migrations.CreateModel(
            name='Family',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
            ],
        ),
        migrations.AlterField(
            model_name='profile',
            name='user_type',
            field=models.PositiveSmallIntegerField(blank=True, choices=[(1, 'Child'), (2, 'Parent'), (3, 'Coach'), (4, 'Admin')], null=True),
        ),
    ]