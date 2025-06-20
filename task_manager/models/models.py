from django.db import models
from .base import TaskModel
from .enums import Weekday


class Task(TaskModel):
    due_date = models.DateTimeField(null=True, blank=True)


class DailyTask(TaskModel):
    weekdays = models.JSONField(default=list)
    is_active = models.BooleanField(default=True)

    def get_weekday_display(self):
        return [Weekday(label).label for label in self.weekdays]


class TaskInstance(TaskModel):
    parent_daily_task = models.ForeignKey(
        DailyTask, on_delete=models.CASCADE, related_name="instances"
    )
    date = models.DateField()

    class Meta:  # type: ignore
        unique_together = ("parent_daily_task", "date")
        ordering = ["-date"]

    def __str__(self):
        return f"{self.title} for {self.date} ({self.user.email})"
