from datetime import timedelta

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from rest_framework.test import APIClient

from auths.models import CustomUser, OTPRecord


class OTPEdgeCasesTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = CustomUser.objects.create_user(
            email="edge@example.com", password="123456"
        )
        self.client.force_authenticate(user=self.user)

    def test_resend_cooldown(self):
        self.client.post("/auths/send-otp/")
        response = self.client.post("/auths/send-otp/")
        self.assertEqual(response.status_code, 429)
        self.assertIn("Wait", response.data["detail"])

    def test_expired_otp(self):
        otp = OTPRecord.objects.create(
            user=self.user,
            code="999999",
            expires_at=timezone.now() - timedelta(minutes=1),
            ip_address="127.0.0.1",
        )
        response = self.client.post("/auths/verify-otp/", {"otp": "999999"})
        self.assertEqual(response.status_code, 400)

    def test_otp_reuse_rejected(self):
        otp = OTPRecord.objects.create(
            user=self.user,
            code="888888",
            expires_at=timezone.now() + timedelta(minutes=5),
            ip_address="127.0.0.1",
        )
        res1 = self.client.post("/auths/verify-otp/", {"otp": "888888"})
        res2 = self.client.post("/auths/verify-otp/", {"otp": "888888"})
        self.assertEqual(res1.status_code, 200)
        self.assertEqual(res2.status_code, 400)
