from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
# Register your models here.


class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'location', 'user_type', 'balance', 'is_staff', 'is_active')
    search_fields = ('username', 'email')
    list_filter = ('user_type', 'is_staff', 'is_active')
    fieldsets = UserAdmin.fieldsets + (
        ('Financial Information', {'fields': ('balance',)}),
    )
    list_editable = ('balance',)


admin.site.register(CustomUser, CustomUserAdmin)
