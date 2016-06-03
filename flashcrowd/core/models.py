from __future__ import unicode_literals

from django.db import models
from django.conf import settings
from django.utils.timezone import now


class Task(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, null=False, blank=False)
    date_created = models.DateTimeField(default=now, null=False, blank=False)
    date_deadline = models.DateTimeField(default=None, null=True, blank=True)


class Call(models.Model):
    STATUSES = (
        ('N', 'New'),
        ('', ''),
    )

    task = models.ForeignKey('Task', null=False, blank=False)
    executor = models.ForeignKey(settings.AUTH_USER_MODEL, null=False, blank=False)
    status = models.CharField(max_length=1, choices=STATUSES, default='N', null=False, blank=False)
    date_accepted = models.DateTimeField(default=now, null=False, blank=False)
