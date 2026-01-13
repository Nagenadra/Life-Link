"""
URL patterns for donors app
"""
from django.urls import path
from . import views

app_name = 'donors'

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('profile/', views.profile, name='profile'),
    path('toggle-availability/', views.toggle_availability, name='toggle_availability'),
    path('schedule/', views.schedule_donation, name='schedule_donation'),
    path('cancel/<int:schedule_id>/', views.cancel_donation, name='cancel_donation'),
]

