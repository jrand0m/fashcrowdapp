# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-06-05 13:45
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0023_auto_20160605_1345'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='badge',
            name='level',
        ),
    ]
