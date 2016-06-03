from __future__ import unicode_literals

from django.db import models
from django.conf import settings
from django.utils.timezone import now


class Task(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, null=False, blank=False)
    date_created = models.DateTimeField(default=now, null=False, blank=False)

