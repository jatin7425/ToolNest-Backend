from decouple import config
from django.contrib import admin
from django.urls import include, path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from toolnest_backend import settings
from functools import wraps
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache


def dynamic_swagger_url(request):
    host = request.get_host()
    scheme = "https" if request.is_secure() else "http"
    return f"{scheme}://{host}/v1"


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
    authentication_classes=[],
)

# Patch Swagger view
swagger_ui_view = method_decorator(never_cache)(
    wraps(schema_view.with_ui("swagger"))(
        lambda request, *args, **kwargs: schema_view.with_ui(
            "swagger", cache_timeout=0
        )(request, *args, **kwargs, url=dynamic_swagger_url(request))
    )
)

# Patch Redoc view
redoc_ui_view = method_decorator(never_cache)(
    wraps(schema_view.with_ui("redoc"))(
        lambda request, *args, **kwargs: schema_view.with_ui("redoc", cache_timeout=0)(
            request, *args, **kwargs, url=dynamic_swagger_url(request)
        )
    )
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("main.urls")),
    path("auths/", include("auths.urls", namespace="auths")),
    path("tasks_manager/", include("task_manager.urls", namespace="task_manager")),
]

if settings.DEBUG or config("ENVIRONMENT", default="dev") == "prod":
    urlpatterns += [
        path("v1/docs/", swagger_ui_view, name="schema-swagger-ui"),
        path("v1/redoc/", redoc_ui_view, name="schema-redoc"),
    ]
