from __future__ import unicode_literals

from django.db import models
from django.conf import settings
from django.utils.timezone import now
from taggit.managers import TaggableManager
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
import re


class Category(models.Model):
    name = models.CharField(max_length=32, null=False, blank=False)
    slug = models.CharField(max_length=32, null=True, blank=True)
    description = models.CharField(max_length=160, null=False, blank=False)
    icon = models.ImageField(upload_to='category', blank=False, null=False)

    def __repr__(self):
        return self.__unicode__()

    def __unicode__(self):
        return u'{} - {}'.format(self.name, self.description or 'No description')


# @staticmethod
def get_default_category():
    return 1


class Task(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, null=False, blank=False, related_name='authored_tasks')
    category = models.ForeignKey(Category, default=get_default_category, null=False, blank=False, related_name='category_tasks')
    description = models.TextField(null=False, blank=False)
    summary = models.TextField(null=False, blank=False, default='')
    date_created = models.DateTimeField(default=now, null=False, blank=False)
    date_deadline = models.DateTimeField(default=None, null=True, blank=True)
    bounty = models.PositiveIntegerField(null=False, blank=False)
    tags = TaggableManager()

    # Nope. Too time-consuming. Not today.
    # @classmethod
    # def new(cls, author, bounty, deadline=None):
    #     return Task.objects.create(author=author, bounty=bounty, deadline=deadline)

    def save(self, *args, **kwargs):
        tags_detected = re.findall(r'\b#\w+', self.description)
        if self.id:
            self.tags.clear()
        for new_tag in tags_detected:
            self.tags.add(new_tag)
        super(Task, self).save(*args, **kwargs)


    def __repr__(self):
        return self.__unicode__()

    def __unicode__(self):
        return u'Task by {} for {} points'.format(self.author, self.bounty)

    def get_final_bounty(self):
        # TODO: This will calculate actual badge bounty based on how many users accepted and rejected the task.
        return self.bounty


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
    validator = models.CharField('validator code', max_length=300, null=False, blank=False, default="False")
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
    level = models.PositiveIntegerField(default=0, null=False, blank=False)

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
        ('task_created', 'Your task is now live!'),  # Deprecated
        ('new_task', 'We have a new task for you!'),  # Task
        ('task_accepted', 'Someone accepted your task!'),  # Deprecated
        ('task_rejected', 'Someone rejected your task.'),  # Deprecated
        ('task_completed', 'Someone completed your task!'),  # Call
        ('proof_accepted', 'Congrats! Creator accepted your proof!'),  # Task
        ('proof_rejected', 'Oops... Creator rejected your proof! :('),  # Task
        ('badge_earned', 'You earned a new badge!')  # Badge
    )

    TYPE_TO_STYLE_MAP = dict(
        task_created='success',
        new_task='info',
        task_accepted='info',
        task_rejected='info',
        task_completed='success',
        proof_accepted='success',
        proof_rejected='danger',
        badge_earned='success'
    )

    TYPE_TO_MESSAGE_MAP = dict(TYPES)

    type = models.CharField(max_length=32, choices=TYPES, null=False, blank=False)
    style = models.CharField(max_length=32, default='info', null=False, blank=False)
    message = models.TextField(null=False, blank=False)
    target_users = models.ManyToManyField(settings.AUTH_USER_MODEL, null=False, blank=False)
    date_created = models.DateTimeField(default=now, null=False, blank=False)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True, blank=True)
    object_id = models.PositiveIntegerField(null=True, blank=True)
    content_object = GenericForeignKey('content_type', 'object_id')

    @classmethod
    def create_new(cls, type, target_users, related_object):
        if not isinstance(target_users, (list, tuple)):
            target_users = [target_users]
        message = Event.TYPE_TO_MESSAGE_MAP.get(type, 'No message. WAT?')
        event = Event(
            type=type,
            style=Event.TYPE_TO_STYLE_MAP.get(type, 'info'),
            message=message,
            content_object=related_object
        )
        event.save()
        for target_user in target_users:
            event.target_users.add(target_user)


class Bookmark(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=False, blank=False, related_name='bookmarks')
    task = models.ForeignKey('Task', null=False, blank=False, related_name='bookmarks')
