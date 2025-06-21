from django.forms import ValidationError
from rest_framework import serializers
from .models.models import Task, DailyTask, TaskInstance
from task_manager.models.enums import Weekday


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = "__all__"
        read_only_fields = ["id", "created_at", "updated_at", "user"]


class DailyTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = DailyTask
        fields = "__all__"
        read_only_fields = ["user", "created_at", "updated_at"]

    def validate_weekdays(self, value):
        for day in value:
            if day not in Weekday.values:
                raise ValidationError(f"Invalid weekday: {day}")
        return value


class TaskInstanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskInstance
        fields = "__all__"
        read_only_fields = ["user", "parent_daily_task", "date"]
