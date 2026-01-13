"""
Authentication views: Login, Register, Home
"""
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from .models import User
from .forms import LoginForm, RegisterForm


def home(request):
    """Home/Landing page"""
    return render(request, 'accounts/home.html')


@require_http_methods(["GET", "POST"])
def user_login(request):
    """Login view with role selection (USERNAME based)"""

    if request.user.is_authenticated:
        return redirect('accounts:login_redirect')

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            role = form.cleaned_data['role']
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = authenticate(
                request,
                username=username,
                password=password
            )

            if user is not None:
                if user.role != role:
                    messages.error(request, 'Selected role does not match this user.')
                else:
                    login(request, user)
                    messages.success(request, f'Welcome back, {user.username}!')
                    return redirect('accounts:login_redirect')
            else:
                messages.error(request, 'Invalid username or password.')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = LoginForm()

    return render(request, 'accounts/login.html', {'form': form})


@require_http_methods(["GET", "POST"])
def user_register(request):
    """Registration view with role selection and location capture"""

    if request.user.is_authenticated:
        return redirect('accounts:login_redirect')

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            latitude = request.POST.get('latitude')
            longitude = request.POST.get('longitude')
            location_name = request.POST.get('location_name', '')

            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])

            if latitude and longitude:
                user.latitude = latitude
                user.longitude = longitude
                user.location_name = location_name

            user.save()

            login(request, user)
            messages.success(
                request,
                f'Registration successful! Welcome to LifeLink, {user.username}!'
            )
            return redirect('accounts:login_redirect')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = RegisterForm()

    return render(request, 'accounts/register.html', {'form': form})


def login_redirect(request):
    """Redirect user to their role-specific dashboard"""

    if not request.user.is_authenticated:
        return redirect('accounts:login')

    if request.user.role == 'donor':
        return redirect('donors:dashboard')
    elif request.user.role == 'bloodbank':
        return redirect('bloodbanks:dashboard')
    elif request.user.role == 'patient':
        return redirect('patients:dashboard')

    return redirect('accounts:home')


def user_logout(request):
    """Logout view"""
    from django.contrib.auth import logout
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('accounts:home')



