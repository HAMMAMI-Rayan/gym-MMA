from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('main.urls')),
    path('cours/', include('cours.urls', namespace='cours')),
    path('entraineurs/', include('entraineurs.urls', namespace='entraineurs')),
    path('membres/', include('membres.urls', namespace='membres')),
    path('reservations/', include('reservations.urls', namespace='reservations')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
