from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from apps.accounts.models import AdminUser


@admin.register(AdminUser)
class AdminUserAdmin(UserAdmin):
    model = AdminUser

    list_display = ("phone", "username", "email", "is_staff")
    ordering = ("phone",)

    fieldsets = (
        (None, {"fields": ("phone", "password")}),
        ("Personal info", {"fields": ("username", "email")}),
        ("Permissions", {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")}),
        ("Important dates", {"fields": ("last_login",)}),
    )

    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("phone", "username", "email", "password1", "password2", "is_staff", "is_superuser"),
        }),
    )

    search_fields = ("phone", "username", "email")
