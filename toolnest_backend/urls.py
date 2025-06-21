from django.contrib import admin
from django.urls import include, path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from toolnest_backend import settings

schema_view = get_schema_view(
    openapi.Info(
        title="Toolnest API",
        default_version="v1",
        description="Auto-generated API docs for Toolnest backend 🧠",
    ),
    public=True,
    permission_classes=[
        permissions.AllowAny if settings.DEBUG else permissions.IsAuthenticated
    ],
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("main.urls")),
    path("auths/", include("auths.urls", namespace="auths")),
    path("tasks_manager/", include("task_manager.urls", namespace="task_manager")),
]

urlpatterns += [
    path(
        "v1/docs/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path(
        "v1/redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"
    ),
]
