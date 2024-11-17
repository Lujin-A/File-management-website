from django import forms
from .models import UploadedFile, Album
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
import re

#---------------------------------------------FILE UPLOAD----------------------------------------------#
class FileUploadForm(forms.ModelForm):
    file = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}), required=False)  # Add the file field
    class Meta:
        model = UploadedFile
        fields = ['labels']  # Let the user fill out the file name and labels

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Adding the custom class directly to the widget
        self.fields['labels'].widget.attrs.update({
            'class': 'upload_labels_form',
            'placeholder': 'Enter tags or labels'
        })

class SignUpForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
        
#------------------------------------------------ALBUM------------------------------------------------#
class AlbumForm(forms.ModelForm):
    class Meta:
        model = Album
        fields = ['album_name', 'display_pattern']

    def clean_album_name(self):
        album_name = self.cleaned_data.get('album_name')
        if not album_name:
            raise ValidationError('Requires album name')
        return album_name

    def clean_display_pattern(self):
        display_pattern = self.cleaned_data.get('display_pattern')
        if not display_pattern:
            raise ValidationError('Requires display pattern')
        return display_pattern

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Adding the custom class directly to the widget
        self.fields['album_name'].widget.attrs.update({
            'class': 'album_name_form',
            'placeholder': 'Enter your chosen album name'
        })

        self.fields['display_pattern'].widget.attrs.update({
            'class': 'album_display_form'
        })


class MediaFileSelectionForm(forms.Form):
    media_files = forms.ModelMultipleChoiceField(
        queryset=UploadedFile.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(MediaFileSelectionForm, self).__init__(*args, **kwargs)
        if user:
            self.fields['media_files'].queryset = UploadedFile.objects.filter(user=user)

    def clean_media_files(self):
        media_files = self.cleaned_data.get('media_files')
        if not media_files:
            raise ValidationError('Requires at least one media file')
        return media_files