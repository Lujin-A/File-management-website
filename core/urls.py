# core/urls.py
from django.urls import path
from . import views  # Import views from the current directory

# Define URL patterns for your core app
urlpatterns = [
    path('', views.home, name='home'),  # Maps the root URL to the home view
]
