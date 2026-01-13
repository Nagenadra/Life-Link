"""
Blood Bank views: Dashboard, Inventory, Scheduled Donors
"""
from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils import timezone
from accounts.decorators import bloodbank_required
from .models import BloodBank, BloodInventory
from donors.models import DonationSchedule


@bloodbank_required
def dashboard(request):
    """Blood Bank dashboard"""
    try:
        blood_bank = BloodBank.objects.get(user=request.user)
    except BloodBank.DoesNotExist:
        # Create profile if it doesn't exist
        blood_bank = BloodBank.objects.create(
            user=request.user,
            address='',
            contact_number=''
        )
    
    # Inventory statistics
    total_units = blood_bank.get_total_units()
    low_stock_alerts = blood_bank.get_low_stock_alerts()
    
    # Today's donations
    today = timezone.now().date()
    today_donations = DonationSchedule.objects.filter(
        blood_bank=blood_bank,
        scheduled_date__date=today,
        status='scheduled'
    ).select_related('donor', 'donor__user')
    
    # Upcoming scheduled donors (next 7 days)
    next_week = timezone.now() + timezone.timedelta(days=7)
    upcoming_donations = DonationSchedule.objects.filter(
        blood_bank=blood_bank,
        scheduled_date__gte=timezone.now(),
        scheduled_date__lte=next_week,
        status='scheduled'
    ).select_related('donor', 'donor__user')[:10]
    
    # Get all inventory items
    inventory_items = BloodInventory.objects.filter(blood_bank=blood_bank).order_by('blood_group')
    
    context = {
        'blood_bank': blood_bank,
        'total_units': total_units,
        'low_stock_alerts': low_stock_alerts,
        'today_donations': today_donations,
        'upcoming_donations': upcoming_donations,
        'inventory_items': inventory_items,
    }
    
    return render(request, 'bloodbanks/dashboard.html', context)


@bloodbank_required
def manage_inventory(request):
    """Manage blood inventory"""
    blood_bank = BloodBank.objects.get(user=request.user)
    
    if request.method == 'POST':
        action = request.POST.get('action')
        blood_group = request.POST.get('blood_group')
        units = int(request.POST.get('units', 0))
        
        if action == 'add':
            inventory, created = BloodInventory.objects.get_or_create(
                blood_bank=blood_bank,
                blood_group=blood_group,
                defaults={'units': 0}
            )
            inventory.units += units
            inventory.save()
            messages.success(request, f'Added {units} units of {blood_group}')
        
        elif action == 'remove':
            try:
                inventory = BloodInventory.objects.get(blood_bank=blood_bank, blood_group=blood_group)
                if inventory.units >= units:
                    inventory.units -= units
                    inventory.save()
                    messages.success(request, f'Removed {units} units of {blood_group}')
                else:
                    messages.error(request, 'Not enough units in inventory')
            except BloodInventory.DoesNotExist:
                messages.error(request, 'Inventory item not found')
        
        elif action == 'update':
            inventory, created = BloodInventory.objects.get_or_create(
                blood_bank=blood_bank,
                blood_group=blood_group,
                defaults={'units': units}
            )
            if not created:
                inventory.units = units
                inventory.save()
            messages.success(request, f'Updated {blood_group} inventory to {units} units')
        
        return redirect('bloodbanks:manage_inventory')
    
    # Get all inventory items
    inventory_items = BloodInventory.objects.filter(blood_bank=blood_bank).order_by('blood_group')
    
    context = {
        'blood_bank': blood_bank,
        'inventory_items': inventory_items,
    }
    
    return render(request, 'bloodbanks/manage_inventory.html', context)


@bloodbank_required
def scheduled_donors(request):
    """View all scheduled donors"""
    blood_bank = BloodBank.objects.get(user=request.user)
    
    # Get all scheduled donations
    scheduled_donations = DonationSchedule.objects.filter(
        blood_bank=blood_bank,
        status='scheduled'
    ).select_related('donor', 'donor__user').order_by('scheduled_date')
    
    # Get completed donations
    completed_donations = DonationSchedule.objects.filter(
        blood_bank=blood_bank,
        status='completed'
    ).select_related('donor', 'donor__user').order_by('-scheduled_date')[:20]
    
    context = {
        'blood_bank': blood_bank,
        'scheduled_donations': scheduled_donations,
        'completed_donations': completed_donations,
    }
    
    return render(request, 'bloodbanks/scheduled_donors.html', context)


@bloodbank_required
def mark_completed(request, schedule_id):
    """Mark a donation as completed"""
    try:
        schedule = DonationSchedule.objects.get(id=schedule_id, blood_bank__user=request.user)
        schedule.mark_completed()
        messages.success(request, 'Donation marked as completed!')
    except DonationSchedule.DoesNotExist:
        messages.error(request, 'Donation schedule not found')
    
    return redirect('bloodbanks:scheduled_donors')

