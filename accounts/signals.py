"""
Signals for automatic profile creation
"""
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User
from donors.models import DonorProfile
from bloodbanks.models import BloodBank


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """Create profile automatically when user is created"""
    if created:
        if instance.role == 'donor':
            # Create donor profile with default values
            # Age and blood_group will be set by user in profile
            DonorProfile.objects.get_or_create(
                user=instance,
                defaults={
                    'blood_group': 'O+',
                }
            )
        elif instance.role == 'bloodbank':
            # Create blood bank profile
            BloodBank.objects.create(
                user=instance,
                address='',
                contact_number='',
            )

