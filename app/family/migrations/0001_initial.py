# Generated by Django 3.0.4 on 2020-03-13 19:32

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Family',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
            ],
            options={
                'verbose_name_plural': 'Families',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Parent',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('title', models.CharField(blank=True, max_length=30)),
                ('family', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='parents', to='family.Family')),
            ],
            options={
                'ordering': ['user__date_joined'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Child',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('family', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='children', to='family.Family')),
            ],
            options={
                'verbose_name_plural': 'Children',
            },
        ),
    ]
