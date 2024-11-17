from django.contrib import admin
from django.urls import path, include
from django.conf import settings  # You are missing this import
from django.conf.urls.static import static  # You have already included this, which is good

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    path('accounts/', include('django.contrib.auth.urls')),  # Django auth URL
]

# Add media URL configuration
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)