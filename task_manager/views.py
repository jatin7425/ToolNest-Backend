# task_manager/views.py
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models.query import QuerySet
from typing import Any
from .models.models import Task
from .serializers import TaskSerializer
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


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
        return Response(
            {"message": "Task deleted successfully"}, status=status.HTTP_200_OK
        )

    @swagger_auto_schema(
        method="patch",
        operation_description="Toggle the completion status of a task",
        responses={200: openapi.Response("Task toggled successfully")},
        request_body=None,
    )
    @action(detail=True, methods=["patch"], url_path="toggle", url_name="toggle")
    def toggle(self, request, pk=None):
        task = self.get_object()
        task.is_completed = not task.is_completed
        task.save()
        return Response(
            {
                "message": f"Task marked as {'completed' if task.is_completed else 'incomplete'}"
            },
            status=status.HTTP_200_OK,
        )
