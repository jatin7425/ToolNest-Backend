from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from django.apps import apps
from django.urls import get_resolver
from django.core.cache import cache


@api_view(["GET"])
def root(request):
    return Response({"message": "Welcome to Toolnest Backend 🚀", "status": "running"})


@api_view(["GET"])
def health(request):
    return Response({"status": "ok", "uptime": "stable", "version": "v1"})


EXCLUDED_APPS = [
    "django",
    "rest_framework",
    "drf_yasg",
    "corsheaders",
    "authtoken",
    "admin",
    "auth",
    "contenttypes",
    "messages",
    "sessions",
    "staticfiles",
    "main",
]

TOOL_DESCRIPTIONS = {
    "task_manager": [
        "Create to-dos",
        "Repeat tasks on set days",
        "Mark tasks as done",
        "Keep daily habits on track",
    ]
}


class InstalledToolsView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        cache_key = "installed_tools_list"
        tools = cache.get(cache_key)

        if tools is None:
            tools = self._build_tools_list()
            cache.set(cache_key, tools, timeout=600)  # Cache for 10 minutes

        return Response(tools)

    def _build_tools_list(self):
        tools = []
        route_map = self._get_route_map()

        for app_config in apps.get_app_configs():
            label = app_config.label
            module = app_config.module.__name__

            if any(module.startswith(ex) or label == ex for ex in EXCLUDED_APPS):
                continue

            tools.append(
                {
                    "title": app_config.verbose_name.replace("_", " ").title(),
                    "name": label,
                    "description": TOOL_DESCRIPTIONS.get(
                        label, "No description available"
                    ),
                    "base_route": route_map.get(label, None),
                }
            )

        return sorted(tools, key=lambda x: x["title"])

    def _get_route_map(self):
        route_map = {}
        for pattern in get_resolver().url_patterns:
            if hasattr(pattern, "namespace") and pattern.namespace:
                label = pattern.namespace
                if label not in EXCLUDED_APPS:
                    route_map[label] = f"/{pattern.pattern}"
        return route_map
