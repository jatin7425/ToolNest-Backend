from datetime import timedelta
from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase

from auths.models import OTPRecord

User = get_user_model()


class AuthFlowTestCase(APITestCase):
    def setUp(self):
        self.signup_url = reverse("auths:signup")
        self.login_url = reverse("auths:login")
        self.otp_url = reverse("auths:send-otp")
        self.verify_url = reverse("auths:verify-otp")
        self.email = "test@example.com"
        self.password = "strongpass123"

    def test_full_auth_flow(self):
        # 1. Sign up
        signup_res = self.client.post(
            self.signup_url, {"email": self.email, "password": self.password}
        )
        self.assertEqual(signup_res.status_code, 201)
        token = signup_res.data["token"]
        self.assertTrue(token)

        # 2. Login
        login_res = self.client.post(
            self.login_url, {"email": self.email, "password": self.password}
        )
        self.assertEqual(login_res.status_code, 200)
        login_token = login_res.data["token"]
        self.assertTrue(login_token)

        # 3. Send OTP (initial)
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {login_token}")
        OTPRecord.objects.all().delete()
        otp_send_1 = self.client.post(self.otp_url)
        self.assertEqual(otp_send_1.status_code, 200)
        self.assertEqual(OTPRecord.objects.filter(user__email=self.email).count(), 1)

        # 4. Fast-forward time using patch on `SendOTPView.post`
        with patch("auths.views.timezone") as mock_tz:
            fake_now = timezone.now() + timedelta(seconds=61)
            mock_tz.now.return_value = fake_now
            otp_send_2 = self.client.post(self.otp_url)
            self.assertEqual(otp_send_2.status_code, 200)

        # 5. Verify OTP using latest code
        otp_code = (
            OTPRecord.objects.filter(user__email=self.email).latest("created_at").code
        )
        otp_verify = self.client.post(self.verify_url, {"otp": otp_code})
        self.assertEqual(otp_verify.status_code, 200)
        self.assertIn("Vault unlocked", otp_verify.data["message"])
