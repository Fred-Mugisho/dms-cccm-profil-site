from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/profil-site/', include('profil_site.urls')),
    path('api/locations/', include('locations.urls')),
    path('api/localisation/', include('localisation.urls')),
    path('api/dashboard/', include('dashboard.urls')),
]
