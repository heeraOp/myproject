from rest_framework import serializers
from django.contrib.auth import authenticate
from apps.accounts.models import AdminUser, PasswordResetOTP
import random


class AdminLoginSerializer(serializers.Serializer):
    phone = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        phone = data.get("phone")
        password = data.get("password")

        user = authenticate(
            request=self.context.get("request"),
            phone=phone,
            password=password,
        )

        if not user:
            raise serializers.ValidationError("Invalid phone or password")

        if not user.is_active:
            raise serializers.ValidationError("User account is disabled")

        data["user"] = user
        return data




class OTPRequestSerializer(serializers.Serializer):
    phone = serializers.CharField()

    def validate_phone(self, phone):
        # Do NOT reveal if phone exists
        self.user = AdminUser.objects.filter(phone=phone).first()
        return phone

    def save(self):
        if not self.user:
            return None

        # Invalidate previous OTPs
        PasswordResetOTP.objects.filter(
            user=self.user,
            is_used=False
        ).update(is_used=True)

        otp = f"{random.randint(100000, 999999)}"

        PasswordResetOTP.objects.create(
            user=self.user,
            otp=otp
        )

        return otp

class OTPVerifySerializer(serializers.Serializer):
    phone = serializers.CharField()
    otp = serializers.CharField(max_length=6)

    def validate(self, data):
        phone = data["phone"]
        otp = data["otp"]

        try:
            user = AdminUser.objects.get(phone=phone)
            otp_obj = PasswordResetOTP.objects.filter(
                user=user,
                otp=otp,
                is_used=False
            ).latest("created_at")
        except (AdminUser.DoesNotExist, PasswordResetOTP.DoesNotExist):
            raise serializers.ValidationError("Invalid OTP")

        if otp_obj.is_expired():
            raise serializers.ValidationError("OTP expired")

        data["user"] = user
        data["otp_obj"] = otp_obj
        return data

class OTPResetPasswordSerializer(serializers.Serializer):
    phone = serializers.CharField()
    otp = serializers.CharField(max_length=6)
    new_password = serializers.CharField(min_length=8)

    def validate(self, data):
        phone = data["phone"]
        otp = data["otp"]

        try:
            user = AdminUser.objects.get(phone=phone)
            otp_obj = PasswordResetOTP.objects.filter(
                user=user,
                otp=otp,
                is_used=False
            ).latest("created_at")
        except (AdminUser.DoesNotExist, PasswordResetOTP.DoesNotExist):
            raise serializers.ValidationError("Invalid OTP")

        if otp_obj.is_expired():
            raise serializers.ValidationError("OTP expired")

        data["user"] = user
        data["otp_obj"] = otp_obj
        return data

    def save(self):
        user = self.validated_data["user"]
        otp_obj = self.validated_data["otp_obj"]
        password = self.validated_data["new_password"]

        user.set_password(password)
        user.save()

        otp_obj.is_used = True
        otp_obj.save()

        return user
