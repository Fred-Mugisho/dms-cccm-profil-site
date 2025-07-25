from django.urls import path
from . import views

urlpatterns = [
    path('', views.locations, name='locations'),
    path('load_locations_from_excel/', views.load_locations_from_excel, name='load_locations_from_excel'),
    
    path('get_province/<int:id>/', views.get_province, name='get_province'),
    path('create_province/', views.create_update_province, name='create_province'),
    path('update_province/<int:id>/', views.create_update_province, name='update_province'),
    
    path('get_territoire/<int:id>/', views.get_territoire, name='get_territoire'),
    path('create_territoire/', views.create_update_territoire, name='create_territoire'),
    path('update_territoire/<int:id>/', views.create_update_territoire, name='update_territoire'),
    
    path('get_secteur/<int:id>/', views.get_secteur, name='get_secteur'),
    path('create_secteur/', views.create_update_secteur, name='create_secteur'),
    path('update_secteur/<int:id>/', views.create_update_secteur, name='update_secteur'),
    
    path('get_groupement/<int:id>/', views.get_groupement, name='get_groupement'),
    path('create_groupement/', views.create_update_groupement, name='create_groupement'),
    path('update_groupement/<int:id>/', views.create_update_groupement, name='update_groupement'),
    
    path('get_village/<int:id>/', views.get_village, name='get_village'),
    path('create_village/', views.create_update_village, name='create_village'),
    path('update_village/<int:id>/', views.create_update_village, name='update_village'),
    
    path('get_zone_sante/<int:id>/', views.get_zone_sante, name='get_zone_sante'),
    path('create_zone_sante/', views.create_update_zone_sante, name='create_zone_sante'),
    path('update_zone_sante/<int:id>/', views.create_update_zone_sante, name='update_zone_sante'),
    
    path('get_aire_sante/<int:id>/', views.get_aire_sante, name='get_aire_sante'),
    path('create_aire_sante/', views.create_update_aire_sante, name='create_aire_sante'),
    path('update_aire_sante/<int:id>', views.create_update_aire_sante, name='update_aire_sante'),
]