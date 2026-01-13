"""
URL patterns for bloodbanks app
"""
from django.urls import path
from . import views

app_name = 'bloodbanks'

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('inventory/', views.manage_inventory, name='manage_inventory'),
    path('scheduled-donors/', views.scheduled_donors, name='scheduled_donors'),
    path('mark-completed/<int:schedule_id>/', views.mark_completed, name='mark_completed'),
]

