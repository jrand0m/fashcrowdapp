# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-06-04 15:03
from __future__ import unicode_literals

from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('core', '0012_merge'),
    ]

    operations = [
        migrations.AlterField(
            model_name='badge',
            name='validator',
            field=models.CharField(default='False', max_length=300, verbose_name='validator code'),
        ),
    ]