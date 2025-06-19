# tel_raqam_code/serializers.py
from rest_framework import serializers
from .models import User

class RegisterSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=15)

    def validate_phone_number(self, value):
        if not value.startswith('+'):
            raise serializers.ValidationError("Telefon raqami + bilan boshlanishi kerak (masalan, +998901234567)")
        return value

class VerifyCodeSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=15)
    code = serializers.CharField(max_length=6)