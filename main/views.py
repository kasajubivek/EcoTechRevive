from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Device
from .forms import LoginForm, RegisterForm

def index(request):
    return render(request, 'main/index.html')

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
            # Process the login form
            pass
    else:
        form = LoginForm()
    return render(request, 'main/user_login.html', {'form': form})

def user_register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            # Process the registration form
            pass
    else:
        form = RegisterForm()
    return render(request, 'main/user_register.html', {'form': form})

def user_history(request):
    # Retrieve user visit history from cookies/sessions
    visits = []
    return render(request, 'main/user_history.html', {'visits': visits})

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
