# Generated by Django 3.1.2 on 2020-10-27 20:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(choices=[('U8', 'Superbaby'), ('U10', 'Mladší predžiaci'), ('U12', 'Starší predžiaci'), ('U14', 'Mladší žiaci'), ('U16', 'Starší žiaci'), ('U18', 'Juniory'), ('U21', 'Dospelý')], max_length=3)),
                ('year_from', models.IntegerField(choices=[(1984, 1984), (1985, 1985), (1986, 1986), (1987, 1987), (1988, 1988), (1989, 1989), (1990, 1990), (1991, 1991), (1992, 1992), (1993, 1993), (1994, 1994), (1995, 1995), (1996, 1996), (1997, 1997), (1998, 1998), (1999, 1999), (2000, 2000), (2001, 2001), (2002, 2002), (2003, 2003), (2004, 2004), (2005, 2005), (2006, 2006), (2007, 2007), (2008, 2008), (2009, 2009), (2010, 2010), (2011, 2011), (2012, 2012), (2013, 2013), (2014, 2014), (2015, 2015), (2016, 2016), (2017, 2017), (2018, 2018), (2019, 2019), (2020, 2020)], default=2018, verbose_name='Year from')),
                ('year_until', models.IntegerField(choices=[(1984, 1984), (1985, 1985), (1986, 1986), (1987, 1987), (1988, 1988), (1989, 1989), (1990, 1990), (1991, 1991), (1992, 1992), (1993, 1993), (1994, 1994), (1995, 1995), (1996, 1996), (1997, 1997), (1998, 1998), (1999, 1999), (2000, 2000), (2001, 2001), (2002, 2002), (2003, 2003), (2004, 2004), (2005, 2005), (2006, 2006), (2007, 2007), (2008, 2008), (2009, 2009), (2010, 2010), (2011, 2011), (2012, 2012), (2013, 2013), (2014, 2014), (2015, 2015), (2016, 2016), (2017, 2017), (2018, 2018), (2019, 2019), (2020, 2020)], default=2020, verbose_name='Year until')),
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
                ('type', models.CharField(choices=[('SKI_TRAINING', 'Ski Training'), ('ATHLETIC_TRAINING', 'Athletic Training'), ('SKI_RACE', 'Ski Race'), ('SKI_CAMP', 'Ski Camp'), ('VIDEO_ANALYZE', 'Video Analyze'), ('MEETING', 'Meeting')], max_length=50)),
                ('canceled', models.BooleanField(default=False)),
                ('send_email', models.BooleanField(default=False)),
                ('start', models.DateTimeField()),
                ('end', models.DateTimeField(blank=True)),
                ('additional_info', models.CharField(blank=True, max_length=150)),
                ('category', models.ManyToManyField(to='events.Category')),
            ],
            options={
                'abstract': False,
                'base_manager_name': 'objects',
            },
        ),
        migrations.CreateModel(
            name='Season',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('year', models.CharField(max_length=9, unique=True)),
                ('current', models.BooleanField(default=False)),
                ('start_date', models.DateField(blank=True, null=True)),
                ('end_date', models.DateField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='SkiRace',
            fields=[
                ('event_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='events.event')),
                ('skis_type', models.CharField(choices=[('ALL', 'All'), ('SL', 'Slalom'), ('GS', 'Giant Slalom')], default='ALL', max_length=3)),
                ('temperature', models.IntegerField(blank=True, null=True)),
                ('propositionURL', models.URLField(blank=True, null=True)),
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
                ('event_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='events.event')),
                ('skis_type', models.CharField(choices=[('ALL', 'All'), ('SL', 'Slalom'), ('GS', 'Giant Slalom')], default='ALL', max_length=3)),
                ('temperature', models.IntegerField(blank=True, null=True)),
                ('gates', models.CharField(blank=True, max_length=50, null=True)),
                ('number_of_runs', models.CharField(blank=True, max_length=50, null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=('events.event',),
        ),
        migrations.CreateModel(
            name='RaceOrganizer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('shorthand', models.CharField(max_length=15)),
                ('website', models.URLField(blank=True, null=True)),
                ('club', models.CharField(blank=True, max_length=50, null=True)),
            ],
            options={
                'unique_together': {('name', 'club')},
            },
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=80)),
                ('ski_slope', models.CharField(blank=True, max_length=50, null=True)),
                ('additional_info', models.CharField(blank=True, max_length=100, null=True)),
            ],
            options={
                'unique_together': {('name', 'ski_slope')},
            },
        ),
        migrations.AddField(
            model_name='event',
            name='location',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='events.location'),
        ),
    ]
