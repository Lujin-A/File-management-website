# core/urls.py

from django.urls import path
from . import views  # Import views from the current directory

from django.contrib.auth import views as auth_views  # Import Django's built-in auth views

urlpatterns = [
    path('', views.home, name='home'),  # Home page
    path('upload/', views.upload_file, name='upload'),  # Upload page
    path('signup/', views.signup, name='signup'),  # Signup page
    path('profile/', views.profile, name='profile'),  # Profile page
    path('login/', auth_views.LoginView.as_view(), name='login'),  # Login page
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),  # Logout URL
    path('upload_success/', views.upload_success, name='upload_success'),  # Success page
    path('files/', views.list_uploaded_files, name='list_uploaded_files'),  # List user's files
    path('files/edit/<int:file_id>/', views.edit_uploaded_file, name='edit_uploaded_file'),  # Edit file details
    path('files/delete/<int:file_id>/', views.delete_uploaded_file, name='delete_uploaded_file'),  # Delete file
]
