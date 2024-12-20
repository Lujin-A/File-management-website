from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import os
from .forms import FileUploadForm
from .models import UploadedFile
from django.conf import settings
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login


def home(request):
    return render(request, 'core/home.html')

# File Upload View to handle multiple files and metadata extraction
@login_required
def upload_file(request):
    if request.method == 'POST':
        # Pass both request.POST and request.FILES to the form
        form = FileUploadForm(request.POST, request.FILES)

        print("POST request received.")
        print("Files received:", request.FILES)

        # Check if form is valid
        if form.is_valid():
            print("Form is valid.")
            
            # Get the list of files from the 'file' field
            files = request.FILES.getlist('file')
            if files:
                for file in files:
                    file_name = file.name  # Original file name
                    file_type = file.content_type.split('/')[1]  # Extract file type
                    file_size = file.size  # Get file size

                    print(f"Processing file: {file_name}, Type: {file_type}, Size: {file_size} bytes")

                    # Create a user-specific directory for storing the uploaded files
                    user_directory = os.path.join(settings.MEDIA_ROOT, f'uploads/{request.user.id}/')
                    if not os.path.exists(user_directory):
                        os.makedirs(user_directory)
                        print(f"Created directory: {user_directory}")

                    # Define the file path to save the file
                    file_location = os.path.join(user_directory, file_name)

                    # Save the file to the user-specific directory
                    try:
                        with open(file_location, 'wb+') as destination:
                            for chunk in file.chunks():
                                destination.write(chunk)
                        print(f"File {file_name} successfully saved to {file_location}")
                    except Exception as e:
                        print(f"Error saving file {file_name}: {e}")
                        messages.error(request, f"Error saving file {file_name}.")
                        continue

                    # Save metadata and file details in the database
                    try:
                        UploadedFile.objects.create(
                            user=request.user,
                            file_name=file_name,
                            file_type=file_type,
                            file_size=file_size,
                            file_location=file_location,
                            labels=request.POST.get('labels')  # Optional labels from the form
                        )
                        print(f"File {file_name} metadata saved to database.")
                    except Exception as e:
                        print(f"Error saving metadata for file {file_name}: {e}")
                        messages.error(request, f"Error saving metadata for file {file_name}.")
                        continue

                # Redirect to the success page after upload
                return redirect('upload_success')
            else:
                print("No files found.")
                messages.error(request, 'No files selected for upload.')
        else:
            print("Form is invalid.")
            print("Form errors:", form.errors)
            messages.error(request, 'Form is invalid. Please check the fields.')
    else:
        form = FileUploadForm()

    return render(request, 'core/upload.html', {'form': form})

# Success View
def upload_success(request):
    return render(request, 'core/upload_success.html')


# User Registration View
def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            # Authenticate and login the user after registration
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, f'Welcome {username}, your account has been created.')
            return redirect('home')  # Redirect to the home page after registration
    else:
        form = UserCreationForm()

    return render(request, 'core/signup.html', {'form': form})

# Profile View
@login_required
def profile(request):
    return render(request, 'core/profile.html', {'user': request.user})

# Success View
def upload_success(request):
    return render(request, 'core/upload_success.html')


# View to list the files uploaded by the user
@login_required
def list_uploaded_files(request):
    files = UploadedFile.objects.filter(user=request.user)  # Show only the user's files
    return render(request, 'core/file_list.html', {'files': files})

# View to edit the uploaded file details (labels only)
@login_required
def edit_uploaded_file(request, file_id):
    uploaded_file = get_object_or_404(UploadedFile, file_id=file_id, user=request.user)

    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES, instance=uploaded_file)

        # Check if a file was uploaded
        if request.FILES.get('file'):
            uploaded_file.file_name = request.FILES['file'].name
            uploaded_file.file_size = request.FILES['file'].size
            uploaded_file.file_type = request.FILES['file'].content_type

            # Save the new file
            user_directory = os.path.join(settings.MEDIA_ROOT, f'uploads/{request.user.id}/')
            if not os.path.exists(user_directory):
                os.makedirs(user_directory)

            file_location = os.path.join(user_directory, uploaded_file.file_name)
            with open(file_location, 'wb+') as destination:
                for chunk in request.FILES['file'].chunks():
                    destination.write(chunk)
            uploaded_file.file_location = file_location

        if form.is_valid():
            form.save()
            messages.success(request, 'File details updated successfully.')
            return redirect('list_uploaded_files')
    else:
        form = FileUploadForm(instance=uploaded_file)

    return render(request, 'core/edit_file.html', {'form': form, 'file': uploaded_file})



# View to delete an uploaded file
@login_required
def delete_uploaded_file(request, file_id):
    uploaded_file = get_object_or_404(UploadedFile, file_id=file_id, user=request.user)

    if request.method == 'POST':
        uploaded_file.delete()
        messages.success(request, 'File deleted successfully.')
        return redirect('list_uploaded_files')  # Redirect back to the list

    return render(request, 'core/confirm_delete.html', {'file': uploaded_file})



