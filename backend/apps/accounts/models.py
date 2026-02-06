from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
    BaseUserManager,
)
from django.utils import timezone


# --------------------------------------------------
# Custom Manager
# --------------------------------------------------
class AdminUserManager(BaseUserManager):
    def create_user(self, phone, username, email, password=None):
        if not phone:
            raise ValueError("Phone number is required")
        if not username:
            raise ValueError("Username is required")
        if not email:
            raise ValueError("Email is required")

        email = self.normalize_email(email)

        user = self.model(
            phone=phone,
            username=username,
            email=email,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone, username, email, password):
        user = self.create_user(phone, username, email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


# --------------------------------------------------
# Admin User Model
# --------------------------------------------------
class AdminUser(AbstractBaseUser, PermissionsMixin):
    phone = models.CharField(
        max_length=15,
        unique=True,
        help_text="Admin phone number (used for login)",
    )

    username = models.CharField(
        max_length=150,
        unique=True,
    )

    email = models.EmailField(
        unique=True,
    )

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    date_joined = models.DateTimeField(default=timezone.now)

    objects = AdminUserManager()

    USERNAME_FIELD = "phone"
    REQUIRED_FIELDS = ["username", "email"]

    def __str__(self):
        return f"{self.username} ({self.phone})"

class PasswordResetOTP(models.Model):
    user = models.ForeignKey(
        AdminUser,
        on_delete=models.CASCADE,
        related_name="password_otps",
    )

    otp = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    is_used = models.BooleanField(default=False)

    class Meta:
        indexes = [
            models.Index(fields=["otp"]),
        ]

    def is_expired(self):
        return timezone.now() > self.created_at + timezone.timedelta(minutes=5)

    def __str__(self):
        return f"OTP for {self.user.phone}"
