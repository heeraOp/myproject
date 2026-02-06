from django.urls import path
from apps.accounts.views import (OTPRequestView,
                                OTPVerifyView,
                                OTPResetPasswordView,
                                AdminLoginView,)

urlpatterns = [
    path("login/", AdminLoginView.as_view(), name="admin-login"),
    path("otp/request/", OTPRequestView.as_view()),
    path("otp/verify/", OTPVerifyView.as_view()),
    path("otp/reset-password/", OTPResetPasswordView.as_view()),
]
