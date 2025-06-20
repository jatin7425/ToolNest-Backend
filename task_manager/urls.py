# task_manager/urls.py
from rest_framework.routers import DefaultRouter
from .views import TaskViewSet

app_name = "tasks_manager"

router = DefaultRouter()
router.register(r"tasks", TaskViewSet, basename="tasks")

urlpatterns = router.urls
