from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView
from django.contrib.auth import authenticate, login, logout
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

# Login functionality for the user
# It uses he User model provided by Django framework
# and makes sure to display an error in case of
# invalid username and/or password.
def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            if not username or not password:
                messages.error(request, 'Invalid username or password.')
            else:
                user = authenticate(username=username, password=password)
                if user is not None:
                    login(request, user)
                    fav_color = request.session.get('fav_color', 'red')
                    request.session.modified = True
                    return redirect('profile')
                else:
                    messages.error(request, 'Invalid username or password.')
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = LoginForm()
    return render(request, 'main/user_login.html', {'form': form})


# Processing the logout request
# making sure to clear the session.
@login_required
def logout_view(request):
    logout(request)
    return redirect('login')  # redirect to login page or any other page you prefer


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


@login_required
# def user_history(request):
#     if request.method == 'POST':
#         form = UserHistoryForm(request.POST)
#         if form.is_valid():
#             # Process the user session data
#             pass
#     else:
#         form = UserHistoryForm()
#     return render(request, 'main/user_history.html', {'form': form})


def search_results(request):
    query = request.GET.get('q')
    # Perform search based on query
    results = []
    page_view(request, 'Search')
    return render(request, 'main/search_results.html', {'results': results})


def contact_us(request):
    page_view(request, 'Contact Us')
    return render(request, 'main/contact_us.html')


def about_us(request):
    page_view(request, 'About Us')
    return render(request, 'main/about_us.html')


def team_details(request):
    return render(request, 'main/team_details.html')



def page_view(request, page_name):
    page_counts = request.session.get('page_counts', {})
    page_counts[page_name] = page_counts.get(page_name, 0) + 1
    request.session['page_counts'] = page_counts


def history(request):
    page_counts = request.session.get('page_counts', {})
    page_visits = [{'page_name': page_name, 'visit_count': count} for page_name, count in page_counts.items()]

    page_visits_sorted = sorted(page_visits, key=lambda x: x['visit_count'], reverse=True)

    return render(request, 'main/history.html', {'page_visits': page_visits_sorted})
