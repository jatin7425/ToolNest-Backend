from datetime import timedelta
from django.utils import timezone
from rest_framework import viewsets, permissions, status
from rest_framework.views import APIView
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models.query import QuerySet
from typing import Any
from .models.models import Task, DailyTask, TaskInstance
from .serializers import TaskInstanceSerializer, TaskSerializer, DailyTaskSerializer
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .tasks import generate_task_instances_for_week


class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self) -> QuerySet[Any]:
        queryset = Task.objects.filter(user=self.request.user)

        title = self.request.query_params.get("title")
        priority = self.request.query_params.get("priority")
        is_completed = self.request.query_params.get("is_completed")

        if title:
            queryset = queryset.filter(title__icontains=title)
        if priority:
            queryset = queryset.filter(priority=priority)
        if is_completed is not None:
            if is_completed.lower() in ["true", "false"]:
                queryset = queryset.filter(is_completed=is_completed.lower() == "true")

        return queryset

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=["post"], url_path="toggle-complete")
    def toggle_complete(self, request, pk=None):
        task = self.get_object()
        task.is_completed = not task.is_completed
        task.save()

        serializer = self.get_serializer(task)
        return Response(serializer.data, status=status.HTTP_200_OK)


class DailyTaskViewSet(viewsets.ModelViewSet):
    serializer_class = DailyTaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return DailyTask.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        task = serializer.save(user=self.request.user)
        generate_task_instances_for_week.delay(task.id)

    @action(detail=True, methods=["post"], url_path="toggle-complete")
    def toggle_complete(self, request, pk=None):
        daily_task = self.get_object()
        daily_task.is_active = not daily_task.is_active
        daily_task.save()

        serializer = self.get_serializer(daily_task)
        return Response(serializer.data, status=status.HTTP_200_OK)


class TaskInstanceViewSet(viewsets.ModelViewSet):
    queryset = TaskInstance.objects.all()
    serializer_class = TaskInstanceSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    @action(detail=True, methods=["post"], url_path="toggle-complete")
    def toggle_complete(self, request, pk=None):
        instance = self.get_object()
        instance.is_completed = not instance.is_completed
        instance.save()
        return Response(self.get_serializer(instance).data)


class TaskStatsView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        today = timezone.localdate()
        week_ago = today - timedelta(days=7)

        tasks = Task.objects.filter(user=user)
        daily_instances = TaskInstance.objects.filter(user=user, date__gte=week_ago)

        completed_today = tasks.filter(
            is_completed=True, updated_at__date=today
        ).count()
        pending_today = tasks.filter(is_completed=False, due_date=today).count()

        week_total = daily_instances.count()
        week_done = daily_instances.filter(is_completed=True).count()

        return Response(
            {
                "completed_today": completed_today,
                "pending_today": pending_today,
                "weekly_completion_rate": f"{(week_done / week_total * 100) if week_total else 0:.1f}%",
                "streak_days": self.get_streak_days(user, today),
            }
        )

    def get_streak_days(self, user, today):
        streak = 0
        for i in range(0, 30):
            day = today - timedelta(days=i)
            if TaskInstance.objects.filter(
                user=user, date=day, is_completed=True
            ).exists():
                streak += 1
            else:
                break
        return streak
