from django.db import models
from django.contrib.auth.models import User

class UploadedFile(models.Model):
    file_id = models.AutoField(primary_key=True)  # This will be the primary key
    user = models.ForeignKey(User, on_delete=models.CASCADE, db_column='user_id')  # Link to the user who uploaded the file
    file_type = models.CharField(max_length=10)
    file_name = models.CharField(max_length=255)
    file_size = models.BigIntegerField()
    file_location = models.CharField(max_length=255)
    upload_date_time = models.DateTimeField(auto_now_add=True)
    labels = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        db_table = 'file_uploaded'

class Profile(models.Model):
    USER_ROLES = [
        ('viewer', 'Viewer'),
        ('uploader', 'Uploader'),
        ('admin', 'Administrator'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=50, choices=USER_ROLES, default='viewer')
    created_at = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'users'  # This sets the custom table name to 'users'

    def __str__(self):
        return f'{self.user.username} - {self.role}'
    
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    try:
        instance.profile.save()
    except Profile.DoesNotExist:
        # Create the profile if it doesn't exist
        Profile.objects.create(user=instance)