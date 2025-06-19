from django.urls import path
from .views import root, health

urlpatterns = [
    path('', root, name="root"),
    path('health/', health, name="health-check"),
]
