"""
Role-Based Access Control (RBAC) Decorators
"""
from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages


def role_required(allowed_roles):
    """
    Decorator to restrict access based on user role
    
    Usage:
        @role_required(['donor'])
        def donor_dashboard(request):
            ...
    """
    def decorator(view_func):
        @wraps(view_func)
        def wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated:
                messages.error(request, 'Please login to access this page.')
                return redirect('accounts:login')
            
            if request.user.role not in allowed_roles:
                messages.error(request, 'You do not have permission to access this page.')
                # Redirect based on user's role
                if request.user.role == 'donor':
                    return redirect('donors:dashboard')
                elif request.user.role == 'bloodbank':
                    return redirect('bloodbanks:dashboard')
                elif request.user.role == 'patient':
                    return redirect('patients:dashboard')
                return redirect('accounts:home')
            
            return view_func(request, *args, **kwargs)
        return wrapped_view
    return decorator


def donor_required(view_func):
    """Decorator to ensure user is a donor"""
    return role_required(['donor'])(view_func)


def bloodbank_required(view_func):
    """Decorator to ensure user is a blood bank"""
    return role_required(['bloodbank'])(view_func)


def patient_required(view_func):
    """Decorator to ensure user is a patient"""
    return role_required(['patient'])(view_func)

