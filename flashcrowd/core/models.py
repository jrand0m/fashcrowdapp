from __future__ import unicode_literals

from django.db import models
from django.conf import settings
from django.utils.timezone import now


class Task(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, null=False, blank=False, related_name='authored_tasks')
    description = models.TextField(null=False, blank=False)
    summary = models.TextField(null=False, blank=False, default='')
    date_created = models.DateTimeField(default=now, null=False, blank=False)
    date_deadline = models.DateTimeField(default=None, null=True, blank=True)
    bounty = models.PositiveIntegerField(null=False, blank=False)


    # Nope. Too time-consuming. Not today.
    # @classmethod
    # def new(cls, author, bounty, deadline=None):
    #     return Task.objects.create(author=author, bounty=bounty, deadline=deadline)

    def save(self, *args, **kwargs):
        # Logic comes here
        super(Task, self).save(*args, **kwargs)

    def __repr__(self):
        return self.__unicode__()

    def __unicode__(self):
        return u'Task by {} for {} points'.format(self.author, self.bounty)

    def get_final_bounty(self):
        # TODO: This will calculate actual badge bounty based on how many users accepted and rejected the task.
        raise NotImplementedError()


class Call(models.Model):
    STATES = (
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
        ('completed', 'Completed'),
        ('won', 'Succeeded'),
        ('lost', 'Failed'),
    )

    task = models.ForeignKey('Task', null=False, blank=False, related_name='calls')
    executor = models.ForeignKey(settings.AUTH_USER_MODEL, null=False, blank=False, related_name='calls')
    date_decided = models.DateTimeField(default=now, null=False, blank=False)
    # is_accepted = models.BooleanField(null=False, blank=False)
    # is_completed = models.BooleanField(default=False, null=False, blank=False)
    state = models.CharField(max_length=16, choices=STATES, null=False, blank=False)
    proof = models.ImageField(null=True, blank=True, upload_to='proofs')

    def save(self, *args, **kwargs):
        # Logic comes here
        super(Call, self).save(*args, **kwargs)

    def __repr__(self):
        return self.__unicode__()

    def __unicode__(self):
        return u'{} {} "{}"'.format(
            self.executor, self.state, self.task
        )


class Badge(models.Model):
    icon = models.ImageField(upload_to='badges', blank=False, null=False)
    name = models.CharField('badge name', max_length=120, blank=False, null=False)
    description = models.CharField('badge description', max_length=300, blank=True, null=False)
    level = models.IntegerField('badge level', null=False, blank=False, default=1)
    # Nope. Too time-consuming. Not today.
    # @classmethod
    # def new(cls, author, bounty, deadline=None):
    #     return Task.objects.create(author=author, bounty=bounty, deadline=deadline)

    def save(self, *args, **kwargs):
        # Logic comes here
        super(Badge, self).save(*args, **kwargs)

    def __repr__(self):
        return self.__unicode__()

    def __unicode__(self):
        return u'{} badge(lvl:{})'.format(self.name, self.level)


class UserBadge(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=False, blank=False, related_name='awarded_user')
    badge = models.ForeignKey(Badge, null=False, blank=False, related_name='awarded_badge')
    award_date = models.DateTimeField(default=now, null=False, blank=False)

    # Nope. Too time-consuming. Not today.
    # @classmethod
    # def new(cls, author, bounty, deadline=None):
    #     return Task.objects.create(author=author, bounty=bounty, deadline=deadline)

    def save(self, *args, **kwargs):
        # Logic comes here
        super(UserBadge, self).save(*args, **kwargs)

    def __repr__(self):
        return self.__unicode__()

    def __unicode__(self):
        return u'{}\'s {} badge (lvl:{})'.format(self.user.username, self.badge.name, self.badge.level)


class Event(models.Model):
    TYPES = (
        ('new_task', 'We have a new task for you!'),
        ('task_accepted', 'Someone accepted your task!'),
        ('task_rejected', 'Someone rejected your task.'),
        ('task_completed', 'Someone completed your task!'),
        ('proof_accepted', 'Congrats! Creator accepted your proof!'),
        ('proof_rejected', 'Oops... Creator rejected your proof! :(')
    )

    TYPE_TO_STYLE_MAP = dict(
        new_task='info',
        task_accepted='info',
        task_rejected='info',
        task_completed='success',
        proof_accepted='success',
        proof_rejected='danger'
    )

    TYPE_TO_MESSAGE_MAP = dict(TYPES)

    type = models.CharField(max_length=32, choices=TYPES, null=False, blank=False)
    style = models.CharField(max_length=32, default='info', null=False, blank=False)
    message = models.TextField(null=False, blank=False)
    target_users = models.ManyToManyField(settings.AUTH_USER_MODEL, null=False, blank=False)
    date_created = models.DateTimeField(default=now, null=False, blank=False)

    @classmethod
    def create_new(self, type, target_users):
        if not isinstance(target_users, (list, tuple)):
            target_users = [target_users]
        event = Event(
            type=type,
            style=Event.TYPE_TO_STYLE_MAP.get(type, 'info'),
            message=Event.TYPE_TO_MESSAGE_MAP.get(type, 'No message. WAT?')
        )
        event.save()
        for target_user in target_users:
            event.target_users.add(target_user)
