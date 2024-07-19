from django.urls import path, include
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

from main import views
from main.views import user_register, user_profile, edit_profile
from django.urls import path
from django.utils import timezone  # Import timezone



def set_restart_flag():
    from django.contrib.sessions.models import Session
    Session.objects.all().update(expire_date=timezone.now())


set_restart_flag()

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('main.urls')),
    path('accounts/login/', views.user_login, name='login'),
    path('accounts/profile/', user_profile, name='profile'),
    path('accounts/edit_profile/', edit_profile, name='edit_profile'),  # Add this line
    # path('contact/', views.contact_us, name='contact'), 
    # other paths
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
