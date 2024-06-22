from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Device
from .forms import LoginForm, RegisterForm, UploadFileForm, UserHistoryForm, EditProfileForm


def index(request):
    return render(request, 'main/index.html')


@login_required
def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            # Process the file upload
            form.save()
            return redirect('index')
    else:
        form = UploadFileForm()
    return render(request, 'main/upload.html', {'form': form})


class DeviceListView(ListView):
    model = Device
    template_name = 'main/device_list.html'
    context_object_name = 'devices'


class DeviceDetailView(DetailView):
    model = Device
    template_name = 'main/device_detail.html'


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('index')
            else:
                messages.error(request, 'Invalid username or password.')
    else:
        form = LoginForm()
    return render(request, 'main/user_login.html', {'form': form})


def user_register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            try:
                User.objects.create_user(username=username, email=email, password=password)
                messages.success(request, 'Account created successfully. Please log in.')
                return redirect('login')  # Redirect to the login page
            except Exception as e:
                messages.error(request, f'Error creating account: {e}')
        else:
            messages.error(request, 'Invalid form. Please correct the errors.')
    else:
        form = RegisterForm()
    return render(request, 'main/user_register.html', {'form': form})


@login_required
def user_profile(request):
    return render(request, 'main/profile.html')


@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully.')
            return redirect('profile')
    else:
        form = EditProfileForm(instance=request.user)
    return render(request, 'main/edit_profile.html', {'form': form})


def user_history(request):
    if request.method == 'POST':
        form = UserHistoryForm(request.POST)
        if form.is_valid():
            # Process the user session data
            pass
    else:
        form = UserHistoryForm()
    return render(request, 'main/user_history.html', {'form': form})


def search_results(request):
    query = request.GET.get('q')
    # Perform search based on query
    results = []
    return render(request, 'main/search_results.html', {'results': results})


def contact_us(request):
    return render(request, 'main/contact_us.html')


def about_us(request):
    return render(request, 'main/about_us.html')


def team_details(request):
    return render(request, 'main/team_details.html')
