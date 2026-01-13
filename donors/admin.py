"""
Admin configuration for donors app
"""
from django.contrib import admin
from .models import DonorProfile, DonationSchedule


@admin.register(DonorProfile)
class DonorProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'blood_group', 'age', 'availability', 'total_donations', 'last_donation_date')
    list_filter = ('blood_group', 'availability')
    search_fields = ('user__username', 'user__email')


@admin.register(DonationSchedule)
class DonationScheduleAdmin(admin.ModelAdmin):
    list_display = ('donor', 'blood_bank', 'scheduled_date', 'status', 'created_at')
    list_filter = ('status', 'scheduled_date')
    search_fields = ('donor__user__username', 'blood_bank__user__username')

