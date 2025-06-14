from django.urls import path
from . import views

urlpatterns = [
    path('', views.localisations, name='localisations'),
    path('<int:id>/', views.get_localisation, name='localisation_detail'),
    path('create/', views.create_update_localisation, name='create_localisation'),
    path('update/<int:id>/', views.create_update_localisation, name='update_localisation'),
]