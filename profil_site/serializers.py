from .models import *
from rest_framework import serializers

# SERIALIZER FOR INFORMATION GENERALE
class InformationGeneraleProfilSiteSerializer(serializers.ModelSerializer):
    class Meta:
        model = InformationGeneraleProfilSite
        fields = [
            'id',
            'siteId',
            'nom_site',
            'site',
            'gestionnaireId',
            'nom_gestionnaire',
            'gestionnaire',
            'coordinateurId',
            'nom_coordinateur',
            'coordinateur',
            'nb_menages',
            'nb_individus',
            'latitude',
            'longitude',
            'code_enqueteur',
            'autres_data',
            'created_at',
            'updated_at',
        ]
        read_only_fields = [
            'site',
            'gestionnaire',
            'coordinateur',
            'autres_data',
            'created_at',
            'updated_at',
        ]
        
class GestionSiteSerializer(serializers.ModelSerializer):
    class Meta:
        model = GestionSite
        fields = [
            'id',
            'profil',
            'bureau_dedie',
            'nb_hommes_gestion',
            'nb_femmes_gestion',
            'comites_present',
            'comites_eliges_par_population',
            'comites_formes',
            'reunions_organisees',
            'comites_representatifs',
            'comites_gestion',
            'created_at',
            'updated_at'
        ]
        
class WashSiteSerializer(serializers.ModelSerializer):
    class Meta:
        model = WashSite
        fields = [
            'id',
            'profil',
            'qte_eau_litres_par_personne',
            'source_principale_eau',
            'signes_defecation_air_libre',
            'jours_sans_eau_potable',
            'savon_disponible',
            'inondations_dommages',
            'methode_elimination_dechets',
            'types_latrines_fonctionnelles',
            'types_douches_fonctionnelles',
            'douches_separees',
            'latrines_vidangees',
            'date_derniere_vidange',
            'eclairage_latrines_douches',
            'installation_adaptees_handicapes',
            'created_at',
            'updated_at',
        ]
        
class SanteSiteSerializer(serializers.ModelSerializer):
    class Meta:
        model = SanteSite
        fields = [
            'id',
            'profil',
            'prestataire_disponible',
            'prestataire_dans_site',
            'service_urgence',
            'service_chirurgie',
            'service_pediatrie',
            'service_prenatal',
            'enfants_non_vaccines',
            'problemes_sante',
            'obsacles_acces',
            'created_at',
            'updated_at',
        ]