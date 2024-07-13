# main/urls.py

from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.user_register, name='register'),
    path('upload/', views.upload_file, name='upload_file'),
    # path('history/', views.user_history, name='user_history'),
    path('devices/', views.DeviceListView.as_view(), name='device_list'),
    path('device/<int:pk>/', views.DeviceDetailView.as_view(), name='device_detail'),
    path('search/', views.search_results, name='search'),
    path('contact/', views.contact_us, name='contact_us'),
    path('about/', views.about_us, name='about_us'),
    path('team/', views.team_details, name='team_details'),
    path('profile/', views.user_profile, name='profile'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('password-reset/', views.password_reset_security_question, name='password_reset'),
    path('password-reset/new-password/', views.set_new_password, name='password_reset_new_password'),
    path('history/', views.history, name='history'),
    # path('add-to-cart/<int:pk>/', views.add_to_cart_view, name='add_to_cart'),
    path('contact-success/', views.contact_success, name='contact_success'),
    path('add-product/', views.add_product, name='add_product'),
    path('shop/', views.shop, name='shop'),
    path('add_to_cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cart_detail, name='cart_detail'),
    path('delete_cart_item/<int:item_id>/', views.delete_cart_item, name='delete_cart_item'),
    path('increase_quantity/<int:item_id>/', views.increase_quantity, name='increase_quantity'),
    path('decrease_quantity/<int:item_id>/', views.decrease_quantity, name='decrease_quantity'),
    path('create_order/', views.create_order, name='create_order'),
    path('order/<int:order_id>/', views.order_detail, name='order_detail'),
    path('orders/', views.order_list, name='order_list'),
    path('enquiry/', views.EnquiryRequest, name='enquiry'),
]