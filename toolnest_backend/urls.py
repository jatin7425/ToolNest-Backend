from decouple import config
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
        # contact=openapi.Contact(email="you@example.com"),
        # license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=[
        permissions.AllowAny if settings.DEBUG else permissions.IsAuthenticated
    ],
    authentication_classes=[],
    url=config("PUBLIC_SWAGGER_URL"),
)

urlpatterns = [
    # Django admin
    path("admin/", admin.site.urls),
    # Entry-point routes (/, /health/)
    path("", include("main.urls")),
    path("auths/", include("auths.urls", namespace="auths")),
]

if settings.DEBUG:
    urlpatterns += [
        path(
            "v1/docs/",
            schema_view.with_ui("swagger", cache_timeout=0),
            name="schema-swagger-ui",
        ),
        path(
            "v1/redoc/",
            schema_view.with_ui("redoc", cache_timeout=0),
            name="schema-redoc",
        ),
    ]
