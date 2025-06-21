from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import TaskInstanceViewSet, TaskViewSet, DailyTaskViewSet, TaskStatsView

app_name = "tasks_manager"

router = DefaultRouter()
router.register(r"tasks", TaskViewSet, basename="tasks")
router.register(r"daily-tasks", DailyTaskViewSet, basename="daily-tasks")
router.register(r"task-instances", TaskInstanceViewSet, basename="task-instances")

urlpatterns = [
    path("", include(router.urls)),
    path("insights/", TaskStatsView.as_view(), name="task-insights"),
]
