# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-06-05 11:31
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('core', '0017_task_tags'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='content_type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='contenttypes.ContentType'),
        ),
        migrations.AddField(
            model_name='event',
            name='object_id',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
    ]
