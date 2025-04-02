from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('gym.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    # URL de déconnexion explicite dans le projet principal
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)