from django.contrib import admin
from .models import Usuario
from django.contrib.auth import get_user_model
from django.contrib.auth import admin as auth_admin
# Register your models here.


User = get_user_model()
@admin.register(User)
class UserAdmin(auth_admin.UserAdmin):
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        ("Personal info", {"fields": [("nome", "sobrenome"),("email") ]}),
        (
           "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    )
    list_display = ["username", "nome"]
    search_fields = ["nome"]