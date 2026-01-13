# """
# Donor views: Dashboard, Profile, Scheduling
# """

# from datetime import datetime

# from django.shortcuts import render, redirect, get_object_or_404
# from django.contrib import messages
# from django.utils import timezone

# from accounts.decorators import donor_required
# from accounts.models import User
# from .models import DonorProfile, DonationSchedule
# from bloodbanks.models import BloodBank
# from accounts.utils import get_nearby_users


# @donor_required
# def dashboard(request):
#     """Donor dashboard"""

#     donor_profile, created = DonorProfile.objects.get_or_create(
#         user=request.user,
#         defaults={
#             'age': 18,
#             'blood_group': 'O+'
#         }
#     )

#     upcoming_donations = DonationSchedule.objects.filter(
#         donor=donor_profile,
#         status='scheduled',
#         scheduled_date__gte=timezone.now()
#     ).select_related(
#         'blood_bank', 'blood_bank__user'
#     ).order_by('scheduled_date')[:5]

#     recent_donations = DonationSchedule.objects.filter(
#         donor=donor_profile,
#         status='completed'
#     ).select_related(
#         'blood_bank', 'blood_bank__user'
#     ).order_by('-scheduled_date')[:5]

#     eligible, eligibility_message = donor_profile.is_eligible()

#     context = {
#         'donor_profile': donor_profile,
#         'upcoming_donations': upcoming_donations,
#         'recent_donations': recent_donations,
#         'eligible': eligible,
#         'eligibility_message': eligibility_message,
#     }

#     return render(request, 'donors/dashboard.html', context)


# @donor_required
# def profile(request):
#     """Donor profile view and edit"""

#     donor_profile = DonorProfile.objects.get(user=request.user)

#     if request.method == 'POST':
#         age = request.POST.get('age')
#         blood_group = request.POST.get('blood_group')
#         phone_number = request.POST.get('phone_number')

#         if age:
#             donor_profile.age = int(age)
#         if blood_group:
#             donor_profile.blood_group = blood_group
#         if phone_number:
#             donor_profile.phone_number = phone_number

#         donor_profile.save()
#         messages.success(request, "Profile updated successfully!")
#         return redirect('donors:profile')

#     return render(
#         request,
#         'donors/profile.html',
#         {'donor_profile': donor_profile}
#     )


# @donor_required
# def toggle_availability(request):
#     """Toggle donor availability"""

#     donor_profile = DonorProfile.objects.get(user=request.user)
#     donor_profile.availability = not donor_profile.availability
#     donor_profile.save()

#     status = "ON" if donor_profile.availability else "OFF"
#     messages.success(request, f"Availability set to {status}")
#     return redirect('donors:dashboard')


# @donor_required
# def schedule_donation(request):
#     """Schedule donation with nearby blood banks"""

#     donor_profile = DonorProfile.objects.get(user=request.user)

#     eligible, eligibility_message = donor_profile.is_eligible()
#     if not eligible:
#         messages.error(request, eligibility_message)
#         return redirect('donors:dashboard')

#     # Get nearby blood banks
#     blood_bank_users = User.objects.filter(role='bloodbank')
#     nearby_blood_bank_users = get_nearby_users(
#         request.user,
#         blood_bank_users,
#         max_distance_km=100
#     )

#     blood_banks = []
#     for user in nearby_blood_bank_users:
#         try:
#             blood_bank = BloodBank.objects.get(user=user)
#             blood_banks.append({
#                 'blood_bank': blood_bank,
#                 'distance': user.distance_km
#             })
#         except BloodBank.DoesNotExist:
#             continue

#     if request.method == 'POST':
#         blood_bank_id = request.POST.get('blood_bank')
#         scheduled_date_str = request.POST.get('scheduled_date')

#         if not scheduled_date_str:
#             messages.error(request, "Please select date and time.")
#             return redirect('donors:schedule_donation')

#         try:
#             # Parse datetime-local format: YYYY-MM-DDTHH:MM
#             scheduled_naive = datetime.strptime(
#                 scheduled_date_str, "%Y-%m-%dT%H:%M"
#             )

#             # Convert to timezone-aware datetime
#             scheduled_datetime = timezone.make_aware(
#                 scheduled_naive,
#                 timezone.get_current_timezone()
#             )

#             if scheduled_datetime < timezone.now():
#                 messages.error(
#                     request,
#                     "You cannot schedule a donation in the past."
#                 )
#                 return redirect('donors:schedule_donation')

#             blood_bank = BloodBank.objects.get(id=blood_bank_id)

#             DonationSchedule.objects.create(
#                 donor=donor_profile,
#                 blood_bank=blood_bank,
#                 scheduled_date=scheduled_datetime,
#                 status='scheduled'
#             )

#             messages.success(
#                 request,
#                 f"Donation scheduled successfully for "
#                 f"{scheduled_datetime.strftime('%d %b %Y, %I:%M %p')}!"
#             )
#             return redirect('donors:dashboard')

#         except BloodBank.DoesNotExist:
#             messages.error(request, "Selected blood bank does not exist.")
#         except ValueError:
#             messages.error(request, "Invalid date and time selected.")
#         except Exception as e:
#             messages.error(request, f"Error scheduling donation: {str(e)}")

#     context = {
#         'donor_profile': donor_profile,
#         'blood_banks': blood_banks,
#         'eligible': eligible,
#         'eligibility_message': eligibility_message,
#     }

#     return render(
#         request,
#         'donors/schedule_donation.html',
#         context
#     )


# @donor_required
# def cancel_donation(request, schedule_id):
#     """Cancel a scheduled donation"""

#     schedule = get_object_or_404(
#         DonationSchedule,
#         id=schedule_id,
#         donor__user=request.user
#     )

#     if schedule.status == 'scheduled':
#         schedule.status = 'cancelled'
#         schedule.save()
#         messages.success(request, "Donation cancelled successfully.")
#     else:
#         messages.error(request, "Cannot cancel this donation.")

#     return redirect('donors:dashboard')

"""
Donor views: Dashboard, Profile, Scheduling
"""

from datetime import datetime, timedelta

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils import timezone

from accounts.decorators import donor_required
from accounts.models import User
from .models import DonorProfile, DonationSchedule
from bloodbanks.models import BloodBank
from accounts.utils import get_nearby_users


@donor_required
def dashboard(request):
    """Donor dashboard"""

    donor_profile, created = DonorProfile.objects.get_or_create(
        user=request.user,
        defaults={
            'age': 18,
            'blood_group': 'O+'
        }
    )

    upcoming_donations = DonationSchedule.objects.filter(
        donor=donor_profile,
        status='scheduled',
        scheduled_date__gte=timezone.now()
    ).select_related(
        'blood_bank', 'blood_bank__user'
    ).order_by('scheduled_date')[:5]

    recent_donations = DonationSchedule.objects.filter(
        donor=donor_profile,
        status='completed'
    ).select_related(
        'blood_bank', 'blood_bank__user'
    ).order_by('-scheduled_date')[:5]

    eligible, eligibility_message = donor_profile.is_eligible()

    # ✅ NEW: check if donor already has active scheduled donation
    has_active_schedule = DonationSchedule.objects.filter(
        donor=donor_profile,
        status='scheduled'
    ).exists()

    context = {
        'donor_profile': donor_profile,
        'upcoming_donations': upcoming_donations,
        'recent_donations': recent_donations,
        'eligible': eligible,
        'eligibility_message': eligibility_message,
        'has_active_schedule': has_active_schedule,  # pass to template
    }

    return render(request, 'donors/dashboard.html', context)


@donor_required
def profile(request):
    """Donor profile view and edit"""

    donor_profile = DonorProfile.objects.get(user=request.user)

    if request.method == 'POST':
        age = request.POST.get('age')
        blood_group = request.POST.get('blood_group')
        phone_number = request.POST.get('phone_number')

        if age:
            donor_profile.age = int(age)
        if blood_group:
            donor_profile.blood_group = blood_group
        if phone_number:
            donor_profile.phone_number = phone_number

        donor_profile.save()
        messages.success(request, "Profile updated successfully!")
        return redirect('donors:profile')

    return render(
        request,
        'donors/profile.html',
        {'donor_profile': donor_profile}
    )


@donor_required
def toggle_availability(request):
    """Toggle donor availability"""

    donor_profile = DonorProfile.objects.get(user=request.user)
    donor_profile.availability = not donor_profile.availability
    donor_profile.save()

    status = "ON" if donor_profile.availability else "OFF"
    messages.success(request, f"Availability set to {status}")
    return redirect('donors:dashboard')


@donor_required
def schedule_donation(request):
    """Schedule donation with nearby blood banks"""

    donor_profile = DonorProfile.objects.get(user=request.user)

    eligible, eligibility_message = donor_profile.is_eligible()
    if not eligible:
        messages.error(request, eligibility_message)
        return redirect('donors:dashboard')

    # ❌ BLOCK if already has an active scheduled donation
    if DonationSchedule.objects.filter(
        donor=donor_profile,
        status='scheduled'
    ).exists():
        messages.error(
            request,
            "You already have an active scheduled donation. "
            "Please cancel it before scheduling a new one."
        )
        return redirect('donors:dashboard')

    # ❌ BLOCK if last completed donation < 90 days
    last_completed = DonationSchedule.objects.filter(
        donor=donor_profile,
        status='completed'
    ).order_by('-scheduled_date').first()

    if last_completed:
        days_passed = (timezone.now().date() - last_completed.scheduled_date.date()).days
        if days_passed < 90:
            messages.error(
                request,
                f"You can schedule your next donation after {90 - days_passed} days."
            )
            return redirect('donors:dashboard')

    # Get nearby blood banks
    blood_bank_users = User.objects.filter(role='bloodbank')
    nearby_blood_bank_users = get_nearby_users(
        request.user,
        blood_bank_users,
        max_distance_km=100
    )

    blood_banks = []
    for user in nearby_blood_bank_users:
        try:
            blood_bank = BloodBank.objects.get(user=user)
            blood_banks.append({
                'blood_bank': blood_bank,
                'distance': user.distance_km
            })
        except BloodBank.DoesNotExist:
            continue

    if request.method == 'POST':
        blood_bank_id = request.POST.get('blood_bank')
        scheduled_date_str = request.POST.get('scheduled_date')

        if not scheduled_date_str:
            messages.error(request, "Please select date and time.")
            return redirect('donors:schedule_donation')

        try:
            scheduled_naive = datetime.strptime(
                scheduled_date_str, "%Y-%m-%dT%H:%M"
            )

            scheduled_datetime = timezone.make_aware(
                scheduled_naive,
                timezone.get_current_timezone()
            )

            if scheduled_datetime < timezone.now():
                messages.error(
                    request,
                    "You cannot schedule a donation in the past."
                )
                return redirect('donors:schedule_donation')

            blood_bank = BloodBank.objects.get(id=blood_bank_id)

            DonationSchedule.objects.create(
                donor=donor_profile,
                blood_bank=blood_bank,
                scheduled_date=scheduled_datetime,
                status='scheduled'
            )

            messages.success(
                request,
                f"Donation scheduled successfully for "
                f"{scheduled_datetime.strftime('%d %b %Y, %I:%M %p')}!"
            )
            return redirect('donors:dashboard')

        except BloodBank.DoesNotExist:
            messages.error(request, "Selected blood bank does not exist.")
        except ValueError:
            messages.error(request, "Invalid date and time selected.")
        except Exception as e:
            messages.error(request, f"Error scheduling donation: {str(e)}")

    context = {
        'donor_profile': donor_profile,
        'blood_banks': blood_banks,
        'eligible': eligible,
        'eligibility_message': eligibility_message,
    }

    return render(
        request,
        'donors/schedule_donation.html',
        context
    )


@donor_required
def cancel_donation(request, schedule_id):
    """Cancel a scheduled donation"""

    schedule = get_object_or_404(
        DonationSchedule,
        id=schedule_id,
        donor__user=request.user
    )

    if schedule.status == 'scheduled':
        schedule.status = 'cancelled'
        schedule.save()
        messages.success(request, "Donation cancelled successfully.")
    else:
        messages.error(request, "Cannot cancel this donation.")

    return redirect('donors:dashboard')
