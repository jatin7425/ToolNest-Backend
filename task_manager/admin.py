from django.contrib import admin
from .models.models import Task, DailyTask, TaskInstance


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ("title", "user", "priority", "is_completed", "due_date")
    search_fields = ("title", "user__email")
    list_filter = ("priority", "is_completed", "created_at")


@admin.register(DailyTask)
class DailyTaskAdmin(admin.ModelAdmin):
    list_display = ("title", "user", "is_active", "get_weekday_display")
    list_filter = ("is_active",)


@admin.register(TaskInstance)
class TaskInstanceAdmin(admin.ModelAdmin):
    list_display = ("title", "user", "date", "is_completed", "parent_daily_task")
    list_filter = ("date", "is_completed")
