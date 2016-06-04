from django.contrib import admin
from . import models


class TaskAdmin(admin.ModelAdmin):
    pass


class CallAdmin(admin.ModelAdmin):
    pass


admin.site.register(models.Task, TaskAdmin)
admin.site.register(models.Call, CallAdmin)
admin.site.register(models.Badge, CallAdmin)

