from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(["GET"])
def root(request):
    return Response({
        "message": "Welcome to Toolnest Backend 🚀",
        "status": "running"
    })

@api_view(["GET"])
def health(request):
    return Response({
        "status": "ok",
        "uptime": "stable",
        "version": "v1"
    })
