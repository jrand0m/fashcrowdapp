# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-06-04 13:56
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0010_merge'),
    ]

    operations = [
        migrations.AddField(
            model_name='badge',
            name='validator',
            field=models.CharField(default='True', max_length=300, verbose_name='validator code'),
        ),
    ]
