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

    def grant_points(self, points):
        self.points += points
        self.points_original += points
        self.save()

    def get_display_name(self):
        if self.first_name and self.last_name:
            return u' '.join((self.first_name, self.last_name))
        return self.username

    def get_photo_url(self):
        if self.photo:
            return self.photo.url
        else:
            sa = self.socialaccount_set.first()
            if sa:
                return sa.get_avatar_url()
            else:
                return None
