from django.urls import path

from .views import health, root

urlpatterns = [
    path("", root, name="root"),
    path("health/", health, name="health-check"),
]
