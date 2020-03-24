# Generated by Django 3.0.4 on 2020-03-24 21:25

from django.db import migrations, models
import django.db.models.deletion
import polymorphic.showfields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('family', '0003_auto_20200322_1358'),
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(choices=[('U8', 'Superbaby'), ('U10', 'Mladší predžiaci'), ('U12', 'Starší predžiaci'), ('U14', 'Mladší žiaci'), ('U16', 'Starší žiaci'), ('U18', 'Juniory'), ('U21', 'Dospelý')], max_length=3)),
                ('year_from', models.DateField()),
                ('year_until', models.DateField()),
                ('members', models.ManyToManyField(blank=True, to='family.Child')),
            ],
            options={
                'verbose_name_plural': 'Categories',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('SKI_TRAINING', 'Ski Training'), ('SKI_RACE', 'Ski Race'), ('SKI_CAMP', 'Ski Camp'), ('VIDEO_ANALYZE', 'Video Analyze'), ('MEETING', 'Meeting')], max_length=50)),
                ('name', models.CharField(blank=True, max_length=100)),
                ('canceled', models.BooleanField(default=False)),
                ('start', models.DateTimeField()),
                ('end', models.DateTimeField(blank=True, null=True)),
                ('location', models.CharField(blank=True, max_length=50)),
                ('additional_info', models.CharField(blank=True, max_length=150)),
                ('category', models.ManyToManyField(to='events.Category')),
                ('participants', models.ManyToManyField(blank=True, to='family.Child')),
                ('polymorphic_ctype', models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='polymorphic_events.event_set+', to='contenttypes.ContentType')),
            ],
            options={
                'abstract': False,
                'base_manager_name': 'objects',
            },
            bases=(polymorphic.showfields.ShowFieldType, models.Model),
        ),
        migrations.CreateModel(
            name='Season',
            fields=[
                ('year', models.CharField(max_length=9, primary_key=True, serialize=False, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='SkiRace',
            fields=[
                ('event_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='events.Event')),
                ('skis_type', models.CharField(choices=[('GS', 'Giant Slalom'), ('SL', 'Slalom'), ('AL', 'All')], default='AL', max_length=2)),
                ('weather', models.CharField(blank=True, max_length=100, null=True)),
                ('temperature', models.IntegerField(blank=True, null=True)),
                ('snow_temperature', models.IntegerField(blank=True, null=True)),
                ('hotel_price', models.CharField(blank=True, max_length=50, null=True)),
                ('book_hotel_from', models.DateTimeField(blank=True, null=True)),
                ('book_hotel_to', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=('events.event',),
        ),
        migrations.CreateModel(
            name='SkiTraining',
            fields=[
                ('event_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='events.Event')),
                ('skis_type', models.CharField(choices=[('GS', 'Giant Slalom'), ('SL', 'Slalom'), ('AL', 'All')], default='AL', max_length=2)),
                ('weather', models.CharField(blank=True, max_length=100, null=True)),
                ('temperature', models.IntegerField(blank=True, null=True)),
                ('snow_temperature', models.IntegerField(blank=True, null=True)),
                ('gates', models.CharField(blank=True, max_length=50, null=True)),
                ('number_of_runs', models.CharField(blank=True, max_length=50, null=True)),
                ('ski_slope', models.CharField(blank=True, max_length=50, null=True)),
                ('extra_field_for_ski_training', models.CharField(blank=True, max_length=50, null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=('events.event',),
        ),
        migrations.AddField(
            model_name='event',
            name='season',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='events.Season'),
        ),
        migrations.AddField(
            model_name='category',
            name='season',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='events.Season'),
        ),
        migrations.AlterUniqueTogether(
            name='category',
            unique_together={('season', 'name')},
        ),
    ]
