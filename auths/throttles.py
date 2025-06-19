from rest_framework.throttling import UserRateThrottle


class OTPThrottle(UserRateThrottle):
    scope = "otp"
