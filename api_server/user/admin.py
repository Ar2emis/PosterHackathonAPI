from django.contrib import admin, auth
from .models import *


admin.site.unregister(auth.models.Group)
admin.site.unregister(auth.models.User)


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    pass


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    pass


@admin.register(WatchType)
class WatchTypeAdmin(admin.ModelAdmin):
    pass


@admin.register(Progress)
class ProgressAdmin(admin.ModelAdmin):
    pass


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    pass


class WatchTasksInline(admin.TabularInline):
    model = Watch.tasks.through
    verbose_name = 'task'


@admin.register(Watch)
class WatchAdmin(admin.ModelAdmin):
    inlines = [WatchTasksInline]
    exclude = ['tasks']