# Generated by Django 3.0.6 on 2021-04-28 04:14

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('projects', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Petition',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.IntegerField(unique=True)),
                ('subject', models.CharField(max_length=140)),
                ('message', models.TextField()),
                ('sent_date', models.DateTimeField(auto_now_add=True, verbose_name='date created')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='projects.Project')),
                ('receiver', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='userReceiver', to=settings.AUTH_USER_MODEL)),
                ('sender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='userSender', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-slug'],
            },
        ),
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.IntegerField(unique=True)),
                ('subject', models.CharField(max_length=140)),
                ('message', models.TextField()),
                ('sent_date', models.DateTimeField(auto_now_add=True, verbose_name='date created')),
                ('receiver', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='notificationReceiver', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-slug'],
            },
        ),
    ]
