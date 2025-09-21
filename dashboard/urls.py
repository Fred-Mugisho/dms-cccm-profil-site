from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('refresh_dashboard/', views.refresh_dashboard, name='refresh_dashboard'),
    path('coordinateurs_gestionnaires/', views.coordinateurs_gestionnaires, name='coordinateurs_gestionnaires'),
]