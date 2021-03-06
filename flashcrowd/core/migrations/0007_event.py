# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-06-04 09:45
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0006_task_summary'),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('new_task', 'We have a new task for you!'), ('task_accepted', 'Someone accepted your task!'), ('task_rejected', 'Someone rejected your task.'), ('task_completed', 'Someone completed your task!'), ('proof_accepted', 'Congrats! Creator accepted your proof!'), ('proof_rejected', 'Oops... Creator rejected your proof! :(')], max_length=32)),
                ('style', models.CharField(default='info', max_length=32)),
                ('message', models.TextField()),
                ('date_created', models.DateTimeField(default=django.utils.timezone.now)),
                ('target_users', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
