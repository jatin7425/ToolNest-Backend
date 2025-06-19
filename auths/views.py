import random
from datetime import timedelta

from django.contrib.auth import authenticate
from django.utils import timezone
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import permissions, status
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView

from auths.utils import EmailService

from .models import OTPRecord
from .serializers import LoginSerializer, OTPVerifySerializer, SignupSerializer
from .throttles import OTPThrottle

COOLDOWN_SECONDS = 60


class SignupView(APIView):
    permission_classes = [permissions.AllowAny]

    @swagger_auto_schema(
        request_body=SignupSerializer,
        responses={201: openapi.Response("Signup Successful")},
    )
    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.save()
        token, _ = Token.objects.get_or_create(user=user)

        return Response(
            {
                "message": "Signup successful",
                "token": token.key,
            },
            status=201,
        )


class LoginView(APIView):
    permission_classes = [permissions.AllowAny]

    @swagger_auto_schema(
        request_body=LoginSerializer,
        responses={201: openapi.Response("Signup Successful")},
    )
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = request.data.get("email")
        password = request.data.get("password")
        user = authenticate(request, username=email, password=password)

        if not user:
            return Response(
                {"detail": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED
            )

        token, _ = Token.objects.get_or_create(user=user)
        request.session["otp_verified"] = False  # Clear OTP verification on login

        return Response(
            {
                "token": token.key,
                "message": "Login successful. OTP required to unlock app.",
            }
        )


class SendOTPView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    throttle_classes = [OTPThrottle]

    def post(self, request):
        user = request.user
        ip = request.META.get("REMOTE_ADDR", "")
        now = timezone.now()
        otp = f"{random.randint(100000, 999999)}"
        expires_at = timezone.now() + timedelta(minutes=5)

        recent = (
            OTPRecord.objects.filter(
                user=user,
                ip_address=ip,
                created_at__gte=now - timedelta(seconds=COOLDOWN_SECONDS),
            )
            .order_by("-created_at")
            .first()
        )

        if recent:
            seconds_remaining = COOLDOWN_SECONDS - int(
                (now - recent.created_at).total_seconds()
            )
            return Response(
                {"detail": f"Wait {seconds_remaining}s before requesting another OTP."},
                status=429,
            )

        OTPRecord.objects.create(
            user=user,
            code=otp,
            expires_at=expires_at,
            ip_address=ip,
        )

        EmailService.send_otp_email(user.email, otp)
        print(f"[DEBUG] OTP for {user.email}: {otp}")

        return Response({"message": f"OTP sent to your email (mocked)"}, status=200)


class VerifyOTPView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        request_body=OTPVerifySerializer,
        responses={201: openapi.Response("Signup Successful")},
    )
    def post(self, request):
        serializer = OTPVerifySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        otp_input = request.data.get("otp")
        ip = request.META.get("REMOTE_ADDR", "")
        now = timezone.now()

        otp_entry = (
            OTPRecord.objects.filter(
                user=request.user, code=otp_input, ip_address=ip, expires_at__gte=now
            )
            .order_by("-created_at")
            .first()
        )

        if not otp_entry:
            return Response({"detail": "Invalid or expired OTP."}, status=400)

        request.session["otp_verified"] = True
        otp_entry.delete()  # One-time use

        return Response({"message": "OTP verified. Vault unlocked!"})
