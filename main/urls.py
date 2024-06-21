from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('devices/', views.DeviceListView.as_view(), name='device_list'),
    path('device/<int:pk>/', views.DeviceDetailView.as_view(), name='device_detail'),
    path('login/', views.user_login, name='user_login'),
    path('register/', views.user_register, name='user_register'),
    path('user/history/', views.user_history, name='user_history'),
    path('search/', views.search_results, name='search_results'),
    path('contact/', views.contact_us, name='contact_us'),
    path('about/', views.about_us, name='about_us'),
    path('team/', views.team_details, name='team_details'),
]
