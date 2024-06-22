from django.urls import path, include
from django.contrib import admin
from django.contrib.auth import views as auth_views

from main import views
from main.views import user_register, user_profile, edit_profile

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('main.urls')),
    path('accounts/login/', views.user_login, name='login'),
    path('accounts/profile/', user_profile, name='profile'),
    path('accounts/edit_profile/', edit_profile, name='edit_profile'),  # Add this line
    # other paths
]