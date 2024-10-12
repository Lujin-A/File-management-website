from django import forms
from .models import UploadedFile
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class FileUploadForm(forms.ModelForm):
    file = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}), required=False)  # Add the file field
    class Meta:
        model = UploadedFile
        fields = ['labels']  # Let the user fill out the file name and labels
    

class SignUpForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

