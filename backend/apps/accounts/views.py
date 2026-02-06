from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from apps.accounts.serializers import OTPRequestSerializer, OTPVerifySerializer,OTPResetPasswordSerializer

from apps.accounts.serializers import AdminLoginSerializer


class AdminLoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = AdminLoginSerializer(
            data=request.data,
            context={"request": request},
        )
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data["user"]
        refresh = RefreshToken.for_user(user)

        return Response(
            {
                "access": str(refresh.access_token),
                "refresh": str(refresh),
                "user": {
                    "id": user.id,
                    "phone": user.phone,
                    "username": user.username,
                    "email": user.email,
                },
            },
            status=status.HTTP_200_OK,
        )




class OTPRequestView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = OTPRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        otp = serializer.save()

        # WhatsApp sending will go here later
        # For now: log / print for dev
        if otp:
            print("OTP:", otp)

        return Response({
            "message": "If the phone number exists, an OTP has been sent."
        })

class OTPVerifyView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = OTPVerifySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        return Response({
            "message": "OTP verified successfully"
        })

class OTPResetPasswordView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = OTPResetPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({
            "message": "Password reset successful"
        })
