"""
Donor models: DonorProfile and DonationSchedule
"""
from django.db import models
from django.core.exceptions import ValidationError
from accounts.models import User
from bloodbanks.models import BloodBank
from datetime import date, timedelta


class DonorProfile(models.Model):
    """
    Extended profile for Donors
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
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='donor_profile')
    age = models.PositiveIntegerField(null=True, blank=True)
    blood_group = models.CharField(max_length=3, choices=BLOOD_GROUP_CHOICES, default='O+')
    availability = models.BooleanField(default=True, help_text='Availability ON/OFF toggle')
    last_donation_date = models.DateField(null=True, blank=True)
    total_donations = models.PositiveIntegerField(default=0)
    phone_number = models.CharField(max_length=15, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Donor Profile'
        verbose_name_plural = 'Donor Profiles'
    
    def __str__(self):
        return f"{self.user.username} - {self.blood_group}"
    
    def is_eligible(self):
        """
        Check if donor is eligible to donate blood
        Rules:
        - Must have availability ON
        - Must be at least 90 days since last donation (if any)
        - Age should be between 18-65
        """
        if not self.availability:
            return False, "Availability is turned OFF"
        
        if not self.age:
            return False, "Please update your age in profile"
        
        if self.age < 18 or self.age > 65:
            return False, "Age must be between 18-65 years"
        
        if self.last_donation_date:
            days_since_last_donation = (date.today() - self.last_donation_date).days
            if days_since_last_donation < 90:
                remaining_days = 90 - days_since_last_donation
                return False, f"Must wait {remaining_days} more days before next donation"
        
        return True, "Eligible to donate"
    
    def get_distance_from(self, latitude, longitude):
        """Calculate distance from given coordinates"""
        if not self.user.latitude or not self.user.longitude:
            return None
        
        from accounts.utils import haversine_distance
        return round(haversine_distance(
            float(self.user.latitude), float(self.user.longitude),
            float(latitude), float(longitude)
        ), 2)


class DonationSchedule(models.Model):
    """
    Schedule donations between Donors and Blood Banks
    """
    STATUS_CHOICES = [
        ('scheduled', 'Scheduled'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    donor = models.ForeignKey(DonorProfile, on_delete=models.CASCADE, related_name='scheduled_donations')
    blood_bank = models.ForeignKey(BloodBank, on_delete=models.CASCADE, related_name='scheduled_donations')
    scheduled_date = models.DateTimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='scheduled')
    notes = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Donation Schedule'
        verbose_name_plural = 'Donation Schedules'
        ordering = ['-scheduled_date']
    
    def __str__(self):
        return f"{self.donor.user.username} -> {self.blood_bank.user.username} on {self.scheduled_date.date()}"
    
    def clean(self):
        """Validate donation schedule"""
        # Check if donor is eligible
        eligible, message = self.donor.is_eligible()
        if not eligible:
            raise ValidationError(f"Donor is not eligible: {message}")
        
        # Check if scheduled date is in the future
        from django.utils import timezone
        if self.scheduled_date <= timezone.now():
            raise ValidationError("Scheduled date must be in the future")
    
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
    
    def mark_completed(self):
        """Mark donation as completed and update donor stats"""
        self.status = 'completed'
        self.save()
        
        # Update donor's last donation date and total donations
        self.donor.last_donation_date = date.today()
        self.donor.total_donations += 1
        self.donor.save()
        
        # Add blood to inventory
        from bloodbanks.models import BloodInventory
        inventory, created = BloodInventory.objects.get_or_create(
            blood_bank=self.blood_bank,
            blood_group=self.donor.blood_group,
            defaults={'units': 0}
        )
        inventory.units += 1
        inventory.save()

