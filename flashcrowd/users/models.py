from __future__ import unicode_literals
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.utils.timezone import now


class CustomUser(AbstractUser):
    class Meta:
        db_table = 'auth_user'
        verbose_name = _('User')
        verbose_name_plural = _('Users')

    photo = models.ImageField(_('Photo'), upload_to='team', blank=True)
    points = models.PositiveIntegerField(default=0, null=False, blank=False)

    # TODO: Replenish points
    points_original = models.PositiveIntegerField(default=0, null=False, blank=False)
    date_points_replenished = models.DateTimeField(default=now, null=False, blank=False)

    USERNAME_FIELD = 'username'
