"""
URL patterns for patients app
"""
from django.urls import path
from . import views

app_name = 'patients'

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('search/', views.search, name='search'),
]

