from django.contrib.auth.backends import ModelBackend
from apps.accounts.models import AdminUser


class PhoneBackend(ModelBackend):
    def authenticate(self, request, phone=None, password=None, **kwargs):
        try:
            user = AdminUser.objects.get(phone=phone)
        except AdminUser.DoesNotExist:
            return None

        if user.check_password(password):
            return user
        return None
