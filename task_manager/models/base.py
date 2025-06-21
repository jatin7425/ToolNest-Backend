# tasks/models/base.py
from django.db import models
from django.conf import settings

PRIORITY_CHOICES = [
    ("very high", "Very High"),
    ("high", "High"),
    ("medium", "Medium"),
    ("low", "Low"),
    ("very low", "Very Low"),
]


class TaskModel(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    priority = models.CharField(
        max_length=10, choices=PRIORITY_CHOICES, default="medium"
    )
    smart_priority = models.BooleanField(default=False)
    postponed_count = models.PositiveIntegerField(default=0)
    is_completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.title} ({self.user.email})"
