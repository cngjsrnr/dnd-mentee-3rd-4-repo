from django.contrib import admin
from .models import User
from django.contrib.auth.admin import UserAdmin


class CustomUserAdmin(UserAdmin):
    list_display = (
        'email',
        'username',
        'is_staff',
    )

    search_fields = (
        'email',
        'username',
    )


admin.site.register(User,CustomUserAdmin)