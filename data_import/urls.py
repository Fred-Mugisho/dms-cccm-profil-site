from django.urls import path
from . import views

urlpatterns = [
    path('', views.import_data, name='import_data'),
    path('export_data/', views.export_data, name='export_data'),
    path('export_sites/', views.export_sites_deplaces, name='export_sites'),
    path('import_sites/', views.import_sites, name='import_sites'),
    path('generate_users/', views.generate_users, name='generate_users'),
]