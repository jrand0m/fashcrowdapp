from django.contrib import admin
from . import models


class TaskAdmin(admin.ModelAdmin):
    pass


class CallAdmin(admin.ModelAdmin):
    pass


class BadgeAdmin(admin.ModelAdmin):
    pass


class UserBadgeAdmin(admin.ModelAdmin):
    pass


admin.site.register(models.Task, TaskAdmin)
admin.site.register(models.Call, CallAdmin)
admin.site.register(models.Badge, BadgeAdmin)
admin.site.register(models.UserBadge, UserBadgeAdmin)
