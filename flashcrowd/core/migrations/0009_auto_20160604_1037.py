# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-06-04 10:37
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_merge'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='type',
            field=models.CharField(choices=[('task_created', 'Your task is now live!'), ('new_task', 'We have a new task for you!'), ('task_accepted', 'Someone accepted your task!'), ('task_rejected', 'Someone rejected your task.'), ('task_completed', 'Someone completed your task!'), ('proof_accepted', 'Congrats! Creator accepted your proof!'), ('proof_rejected', 'Oops... Creator rejected your proof! :(')], max_length=32),
        ),
    ]
