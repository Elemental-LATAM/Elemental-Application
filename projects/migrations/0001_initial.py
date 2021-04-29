# Generated by Django 3.0.6 on 2021-04-28 04:14

import core.aux
import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('core', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.IntegerField(unique=True)),
                ('title', models.CharField(max_length=100)),
                ('start_date', models.DateTimeField(auto_now_add=True, verbose_name='date created')),
                ('project_date', models.DateTimeField(blank=True, default=datetime.date.today, verbose_name='since')),
                ('summary', models.CharField(max_length=140)),
                ('description', models.TextField()),
                ('image', models.ImageField(blank=True, upload_to='img/projects', validators=[core.aux.validate_file_size])),
                ('admin', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-slug'],
            },
        ),
        migrations.CreateModel(
            name='ProjectInterestCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.IntegerField(unique=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.InterestCategory')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='projects.Project')),
            ],
            options={
                'ordering': ['-slug'],
            },
        ),
        migrations.CreateModel(
            name='ProjectInterest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.IntegerField(unique=True)),
                ('category_slug', models.CharField(default='', max_length=30)),
                ('interest_slug', models.CharField(default='', max_length=30)),
                ('interest', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Interest')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='projects.Project')),
            ],
            options={
                'ordering': ['-slug'],
            },
        ),
        migrations.CreateModel(
            name='Assignation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.IntegerField(unique=True)),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='projects.Project')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-slug'],
            },
        ),
    ]
