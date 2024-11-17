# core/urls.py

from django.urls import path
from . import views  # Import views from the current directory
from django.contrib.auth import views as auth_views  # Import Django's built-in auth views

# urls.py
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    # BASIC
    path('', views.home, name='home'),  # Home page
    path('signup/', views.signup, name='signup'),  # Signup page
    path('profile/', views.profile, name='profile'),  # Profile page
    path('login/', auth_views.LoginView.as_view(), name='login'),  # Login page
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),  # Logout URL

    # FILE UPLOAD MANAGEMENT
    path('upload/', views.upload_file, name='upload'),  # Upload page
    path('upload_success/', views.upload_success, name='upload_success'),  # Success page
    path('files/', views.list_uploaded_files, name='list_uploaded_files'),  # List user's files
    path('files/edit/<int:file_id>/', views.edit_uploaded_file, name='edit_uploaded_file'),  # Edit file details
    path('files/delete/<int:file_id>/', views.delete_uploaded_file, name='delete_uploaded_file'),  # Delete file
    path('files/batch-delete-confirm/', views.batch_delete_confirm, name='batch_delete_confirm'), # Batch delete files confirmation
    path('files/batch-delete/', views.batch_delete_files, name='batch_delete_files'), # Batch delete

    # ALBUM MANAGEMENT
    path('create-album/', views.create_album, name='create_album'), # Create album
    path('album_success/', views.album_success, name='album_success'),  # Success page
    path('albums/', views.album_list, name='album_list'), # Manage album
    path('edit-album/<int:album_id>/', views.edit_album, name='edit_album'), # Edit album
    path('delete-album/<int:album_id>/', views.delete_album, name='delete_album'), # Delete album
    path('album/<int:album_id>/', views.album_detail, name='album_detail'), # Preview album

    # PLAYBACK MANAGEMENT
    path('playback-management/', views.playback_management, name='playback_management'), # Playback Management
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


