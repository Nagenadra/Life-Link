"""
Admin configuration for accounts app
"""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """Custom admin for User model"""
    list_display = ('username', 'email', 'role', 'location_name', 'is_active', 'date_joined')
    list_filter = ('role', 'is_active', 'is_staff', 'date_joined')
    fieldsets = BaseUserAdmin.fieldsets + (
        ('LifeLink Information', {
            'fields': ('role', 'latitude', 'longitude', 'location_name')
        }),
    )
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ('LifeLink Information', {
            'fields': ('role', 'latitude', 'longitude', 'location_name')
        }),
    )

