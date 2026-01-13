"""
Patient views: Dashboard, Search for Donors and Blood Banks
"""
from django.shortcuts import render, redirect
from django.contrib import messages
from accounts.decorators import patient_required
from accounts.models import User
from accounts.utils import get_nearby_users
from donors.models import DonorProfile
from bloodbanks.models import BloodBank, BloodInventory


@patient_required
def dashboard(request):
    """Patient dashboard"""
    context = {}
    return render(request, 'patients/dashboard.html', context)


@patient_required
def search(request):
    """Search for donors and blood banks by blood group and distance"""
    if not request.user.latitude or not request.user.longitude:
        messages.warning(request, 'Please update your location to search for donors and blood banks.')
        return redirect('patients:dashboard')
    
    blood_group = request.GET.get('blood_group', '')
    max_distance = float(request.GET.get('max_distance', 50))
    availability_only = request.GET.get('availability_only') == 'on'
    
    donors_results = []
    blood_banks_results = []
    
    if blood_group:
        # Search donors
        donor_profiles = DonorProfile.objects.filter(blood_group=blood_group)
        
        if availability_only:
            donor_profiles = donor_profiles.filter(availability=True)
        
        donor_users = User.objects.filter(
            id__in=donor_profiles.values_list('user_id', flat=True)
        )
        
        nearby_donors = get_nearby_users(request.user, donor_users, max_distance_km=max_distance)
        
        for user in nearby_donors:
            try:
                donor_profile = DonorProfile.objects.get(user=user)
                eligible, eligibility_msg = donor_profile.is_eligible()
                
                donors_results.append({
                    'donor': donor_profile,
                    'distance': user.distance_km,
                    'eligible': eligible,
                    'eligibility_msg': eligibility_msg,
                })
            except DonorProfile.DoesNotExist:
                continue
        
        # Search blood banks
        blood_bank_users = User.objects.filter(role='bloodbank')
        nearby_blood_banks = get_nearby_users(request.user, blood_bank_users, max_distance_km=max_distance)
        
        for user in nearby_blood_banks:
            try:
                blood_bank = BloodBank.objects.get(user=user)
                try:
                    inventory = BloodInventory.objects.get(
                        blood_bank=blood_bank,
                        blood_group=blood_group
                    )
                    available_units = inventory.units
                except BloodInventory.DoesNotExist:
                    available_units = 0
                
                blood_banks_results.append({
                    'blood_bank': blood_bank,
                    'distance': user.distance_km,
                    'available_units': available_units,
                })
            except BloodBank.DoesNotExist:
                continue
    
    context = {
        'blood_group': blood_group,
        'max_distance': max_distance,
        'availability_only': availability_only,
        'donors_results': donors_results,
        'blood_banks_results': blood_banks_results,
    }
    
    return render(request, 'patients/search.html', context)

