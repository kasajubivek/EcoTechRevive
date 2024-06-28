from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Device, UserProfile
from .forms import LoginForm, RegisterForm, UploadFileForm, UserHistoryForm, EditProfileForm, PasswordResetForm, SetNewPasswordForm
from django.contrib.auth import update_session_auth_hash

def index(request):
    return render(request, 'main/index.html')

@login_required
def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
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
            if not username or not password:
                messages.error(request, 'Invalid username or password.')
            else:
                user = authenticate(username=username, password=password)
                if user is not None:
                    login(request, user)
                    return redirect('profile')
                else:
                    messages.error(request, 'Invalid username or password.')
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = LoginForm()
    return render(request, 'main/user_login.html', {'form': form})

@login_required
def logout_view(request):
    logout(request)
    return redirect('login')


def user_register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            password = form.cleaned_data['password']
            user.set_password(password)
            user.save()

            # Create UserProfile instance
            UserProfile.objects.create(
                user=user,
                security_question_1=form.cleaned_data['security_question_1'],
                security_answer_1=form.cleaned_data['security_answer_1'],
                security_question_2=form.cleaned_data['security_question_2'],
                security_answer_2=form.cleaned_data['security_answer_2'],
                security_question_3=form.cleaned_data['security_question_3'],
                security_answer_3=form.cleaned_data['security_answer_3']
            )

            messages.success(request, 'Account created successfully. Please log in.')
            return redirect('login')
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
    results = []
    return render(request, 'main/search_results.html', {'results': results})

def contact_us(request):
    return render(request, 'main/contact_us.html')

def about_us(request):
    return render(request, 'main/about_us.html')

def team_details(request):
    return render(request, 'main/team_details.html')

def password_reset_security_question(request):
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            security_answer_1 = form.cleaned_data['security_answer_1']
            security_answer_2 = form.cleaned_data['security_answer_2']
            security_answer_3 = form.cleaned_data['security_answer_3']
            try:
                user = User.objects.get(username=username)
                profile = UserProfile.objects.get(user=user)
                if (profile.security_answer_1 == security_answer_1 and
                    profile.security_answer_2 == security_answer_2 and
                    profile.security_answer_3 == security_answer_3):
                    request.session['reset_user_id'] = user.id
                    return redirect('password_reset_new_password')
                else:
                    form.add_error(None, 'Security answers do not match.')
            except User.DoesNotExist:
                form.add_error('username', 'User does not exist.')
            except UserProfile.DoesNotExist:
                form.add_error('username', 'User profile does not exist.')
    else:
        form = PasswordResetForm()

    return render(request, 'main/password_reset_security_question.html', {'form': form})

def set_new_password(request):
    if request.method == 'POST':
        form = SetNewPasswordForm(request.POST)
        if form.is_valid():
            user_id = request.session.get('reset_user_id')
            if user_id:
                user = get_object_or_404(User, id=user_id)
                user.set_password(form.cleaned_data['new_password'])
                user.save()
                update_session_auth_hash(request, user)
                messages.success(request, 'Password reset successfully. Please log in with your new password.')
                return redirect('login')
            else:
                form.add_error(None, 'Session expired. Please start the password reset process again.')
    else:
        form = SetNewPasswordForm()

    return render(request, 'main/set_new_password.html', {'form': form})
