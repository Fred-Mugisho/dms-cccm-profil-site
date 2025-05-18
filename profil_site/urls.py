from django.urls import path
from . import views

urlpatterns = [
    path('', views.profils_sites, name='profils_sites'),
    path('<int:id>/', views.profils_sites, name='profil_site_detail'),
    path('create/', views.create_profil_site, name='create_profil_site'),
]
