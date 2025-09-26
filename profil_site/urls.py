from django.urls import path
from . import views
from . import profil_complet_views as prof_views
 
urlpatterns = [
    path('options_profil_site/', views.choices_profil_site, name='choices_profil_site'),
    path('', views.profils_sites, name='profils_sites'),
    path('<int:id>/', views.profils_sites, name='profil_site_detail'),
    path('create/', views.create_profil_site, name='create_profil_site'),
    
    # PROFIL DE SITE COMPLET
    path('options_choices/', prof_views.options_choices, name='options_choices'),
    path('complet/', prof_views.profils_sites_complet, name='profils_sites_complet'),
    path('complet/<uuid:id>/', prof_views.profils_sites_complet, name='profil_site_detail_complet'),
    path('create_profil_site/', prof_views.create_profil_site, name='create_profil_site'),
    path('create_gestion_administration', prof_views.create_gestion_administration_profil_site, name='create_gestion_administration_profil_site'),
    path('create_organisation_fonctionnement', prof_views.create_organisation_fonctionnement_profil_site, name='create_organisation_fonctionnement_profil_site'),
    path('create_vulnerabilites', prof_views.create_vulnerabilites_profil_site, name='create_vulnerabilites_profil_site'),
    path('create_abris_ame', prof_views.create_abris_ame_profil_site, name='create_abris_ame_profil_site'),
    path('create_wash', prof_views.create_wash_profil_site, name='create_wash_profil_site'),
    path('create_sante', prof_views.create_sante_profil_site, name='create_sante_profil_site'),
    path('create_securite_alimentaire', prof_views.create_securite_alimentaire_profil_site, name='create_securite_alimentaire_profil_site'),
    path('create_protection', prof_views.create_protection_profil_site, name='create_protection_profil_site'),
    path('create_education', prof_views.create_education_profil_site, name='create_education_profil_site'),
    path('create_moyens_subsistance', prof_views.create_moyens_subsistance_profil_site, name='create_moyens_subsistance_profil_site'),
    path('create_cartographie_acteurs_services', prof_views.create_cartographie_acteurs_services_profil_site, name='create_cartographie_acteurs_services_profil_site'),
]
