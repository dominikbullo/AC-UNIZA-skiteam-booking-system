# Generated by Django 3.0.4 on 2020-03-22 11:42

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('family', '0001_initial'),
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='FamilyMember',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('extra_field_family_member', models.CharField(blank=True, max_length=30)),
                ('family', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='children', to='family.Family')),
            ],
            options={
                'ordering': ['user__date_joined'],
            },
        ),
        migrations.CreateModel(
            name='Child',
            fields=[
                ('familymember_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='family.FamilyMember')),
                ('test_field', models.CharField(blank=True, max_length=30)),
            ],
            options={
                'verbose_name_plural': 'Children',
            },
            bases=('family.familymember',),
        ),
    ]
