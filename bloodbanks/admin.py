"""
Admin configuration for bloodbanks app
"""
from django.contrib import admin
from .models import BloodBank, BloodInventory


@admin.register(BloodBank)
class BloodBankAdmin(admin.ModelAdmin):
    list_display = ('user', 'get_location_name', 'contact_number', 'created_at')
    search_fields = ('user__username', 'user__email', 'address')
    
    def get_location_name(self, obj):
        return obj.user.location_name or 'N/A'
    get_location_name.short_description = 'Location'


@admin.register(BloodInventory)
class BloodInventoryAdmin(admin.ModelAdmin):
    list_display = ('blood_bank', 'blood_group', 'units', 'last_updated')
    list_filter = ('blood_group', 'last_updated')
    search_fields = ('blood_bank__user__username',)

