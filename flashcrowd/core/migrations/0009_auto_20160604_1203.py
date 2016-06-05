# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-06-04 12:03
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
from flashcrowd.core.models import get_default_category


def create_categories(apps, schema):
    category_model = apps.get_model('core.Category')
    category_model.objects.create(name="Mystery")
    category_model.objects.create(name="Selfie")
    category_model.objects.create(name="Stranger")
    category_model.objects.create(name="Geo")
    category_model.objects.create(name="Team")


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_merge'),
    ]

    operations = [

        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32)),
                ('description', models.CharField(max_length=160)),
                ('icon', models.ImageField(upload_to='category')),
            ],
        ),

        migrations.RunPython(create_categories),
        migrations.AlterField(
            model_name='event',
            name='type',
            field=models.CharField(choices=[('task_created', 'Your task is now live!'), ('new_task', 'We have a new task for you!'), ('task_accepted', 'Someone accepted your task!'), ('task_rejected', 'Someone rejected your task.'), ('task_completed', 'Someone completed your task!'), ('proof_accepted', 'Congrats! Creator accepted your proof!'), ('proof_rejected', 'Oops... Creator rejected your proof! :(')], max_length=32),
        ),
        migrations.AddField(
            model_name='task',
            name='category',
            field=models.ForeignKey(default=get_default_category, on_delete=django.db.models.deletion.CASCADE, related_name='category_tasks', to='core.Category'),
        ),
    ]
