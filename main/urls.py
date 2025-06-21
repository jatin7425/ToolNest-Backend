from django.urls import path
from .views import InstalledToolsView, health, root

urlpatterns = [
    path("", root, name="root"),
    path("tools/", InstalledToolsView.as_view(), name="list-installed-tools"),
    path("health/", health, name="health-check"),
]
