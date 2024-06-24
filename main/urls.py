# main/urls.py

from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.user_register, name='register'),
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='password_reset.html'), name='password_reset'),
    path('upload/', views.upload_file, name='upload_file'),
    path('history/', views.user_history, name='user_history'),
    path('devices/', views.DeviceListView.as_view(), name='device_list'),
    path('device/<int:pk>/', views.DeviceDetailView.as_view(), name='device_detail'),
    path('search/', views.search_results, name='search'),
    path('contact/', views.contact_us, name='contact_us'),
    path('about/', views.about_us, name='about_us'),
    path('team/', views.team_details, name='team_details'),
    path('profile/', views.user_profile, name='profile'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
]