from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

class CustomUserAdmin(UserAdmin):
    list_display = ('id', 'email', 'name', 'role', 'phone', 'is_staff')
    list_filter = ('role', 'is_staff', 'is_superuser')
    search_fields = ('email', 'name', 'phone')
    ordering = ('id',)

    # Add custom fields to forms
    fieldsets = UserAdmin.fieldsets + (
        ('Extra Info', {'fields': ('name', 'role', 'phone')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Extra Info', {'fields': ('name', 'role', 'phone')}),
    )

admin.site.register(User, CustomUserAdmin)
