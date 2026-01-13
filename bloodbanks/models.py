"""
Blood Bank models: BloodBankProfile and BloodInventory
"""
from django.db import models
from accounts.models import User


class BloodBank(models.Model):
    """
    Extended profile for Blood Banks
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='blood_bank_profile')
    address = models.TextField()
    contact_number = models.CharField(max_length=15)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Blood Bank'
        verbose_name_plural = 'Blood Banks'
    
    def __str__(self):
        return f"{self.user.username} - {self.user.location_name}"
    
    def get_distance_from(self, latitude, longitude):
        """Calculate distance from given coordinates"""
        if not self.user.latitude or not self.user.longitude:
            return None
        
        from accounts.utils import haversine_distance
        return round(haversine_distance(
            float(self.user.latitude), float(self.user.longitude),
            float(latitude), float(longitude)
        ), 2)
    
    def get_total_units(self):
        """Get total blood units in inventory"""
        return sum(inv.units for inv in self.inventory.all())
    
    def get_low_stock_alerts(self, threshold=10):
        """Get blood groups with low stock"""
        return self.inventory.filter(units__lt=threshold)


class BloodInventory(models.Model):
    """
    Blood inventory for each blood bank
    """
    BLOOD_GROUP_CHOICES = [
        ('A+', 'A+'),
        ('A-', 'A-'),
        ('B+', 'B+'),
        ('B-', 'B-'),
        ('AB+', 'AB+'),
        ('AB-', 'AB-'),
        ('O+', 'O+'),
        ('O-', 'O-'),
    ]
    
    blood_bank = models.ForeignKey(BloodBank, on_delete=models.CASCADE, related_name='inventory')
    blood_group = models.CharField(max_length=3, choices=BLOOD_GROUP_CHOICES)
    units = models.PositiveIntegerField(default=0)
    last_updated = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Blood Inventory'
        verbose_name_plural = 'Blood Inventories'
        unique_together = ['blood_bank', 'blood_group']
    
    def __str__(self):
        return f"{self.blood_bank.user.username} - {self.blood_group}: {self.units} units"
    
    def is_low_stock(self, threshold=10):
        """Check if stock is low"""
        return self.units < threshold

