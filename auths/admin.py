from django.contrib import admin
from rest_framework.authtoken.models import Token

from .models import OTPRecord

# Register your models here
admin.site.register(Token)
admin.site.register(OTPRecord)
