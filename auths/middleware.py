from django.http import JsonResponse


class OTPRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated and not request.session.get("otp_verified"):
            if request.path not in [
                "/auths/send-otp/",
                "/auths/verify-otp/",
                "/admin/",
            ]:
                return JsonResponse(
                    {"detail": "OTP verification required."}, status=401
                )
        return self.get_response(request)
