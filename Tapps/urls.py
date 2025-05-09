#libaries
from django.contrib import admin
from django.urls import path, include
from users import views as user_views
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

# Url patterns
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(('TechMarket.urls', 'techmarket'), namespace='techmarket')),
    path('register/', user_views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
    path('profile/', user_views.profile, name='profile'),
]
# media for development
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)