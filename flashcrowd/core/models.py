from __future__ import unicode_literals

from django.db import models
from django.conf import settings
from django.utils.timezone import now


class Task(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, null=False, blank=False, related_name='authored_tasks')
    date_created = models.DateTimeField(default=now, null=False, blank=False)
    date_deadline = models.DateTimeField(default=None, null=True, blank=True)
    bounty = models.PositiveIntegerField(null=False, blank=False)

    # Nope. Too time-consuming. Not today.
    # @classmethod
    # def new(cls, author, bounty, deadline=None):
    #     return Task.objects.create(author=author, bounty=bounty, deadline=deadline)


class Call(models.Model):
    STATUSES = (
        ('A', 'Accepted'),
        ('R', 'Rejected'),
    )

    task = models.ForeignKey('Task', null=False, blank=False, related_name='calls')
    executor = models.ForeignKey(settings.AUTH_USER_MODEL, null=False, blank=False, related_name='calls')
    status = models.CharField(max_length=1, choices=STATUSES, null=False, blank=False)
    date_decided = models.DateTimeField(default=now, null=False, blank=False)
    is_accepted = models.BooleanField(null=False, blank=False)
    is_completed = models.BooleanField(default=False, null=False, blank=False)
    proof = models.ImageField(null=True, blank=True, upload_to='proofs')
