from ..bases.base_model import BaseModel
from django.db import models
from data_import.models import SiteDeplace
from utils.choices import *
from rest_framework import serializers

class DetailsTypeAbrisProfilSite(BaseModel):
    type_abris = models.CharField(max_length=255)
    nombre_installes = models.PositiveBigIntegerField(default=0)
    nombre_occupees = models.PositiveBigIntegerField(default=0)
    nombre_occupees_maintenance = models.PositiveBigIntegerField(default=0)
    nombre_occupees_remplacement = models.PositiveBigIntegerField(default=0)
    
    def __str__(self):
        return self.type_abris

class AbrisAmesProfilSite(BaseModel):
    site = models.ForeignKey(SiteDeplace, on_delete=models.CASCADE, db_index=True)
    capacite_accueil_max = models.PositiveBigIntegerField(default=0)
    familles_attente_parcelle_abris = models.PositiveBigIntegerField(default=0)
    fermeture_site_prevue = models.CharField(max_length=255, choices=OUI_NON_CHOICES)
    
    types_abris_present = models.TextField() # Separator: ;
    nombre_abris_occupes_maintenance = models.PositiveBigIntegerField(default=0)
    nombre_abris_occupes_remplacement = models.PositiveBigIntegerField(default=0)
    details_types_abris = models.ManyToManyField(DetailsTypeAbrisProfilSite, blank=True)
    
    besoins_en_ames = models.TextField()
    besoins_ames_saison_seche = models.TextField()
    strategies_adaptation_ames = models.TextField()
    
    etat_generale_parcelle_communautaire = models.CharField(max_length=255)
    etat_generale_routes = models.CharField(max_length=255)
    etat_generale_canaux_evacuations_eaux_pluviales = models.CharField(max_length=255)
    inodations_derniers_saison = models.CharField(max_length=255, choices=OUI_NON_CHOICES)
    nombre_incendies_ce_mois = models.PositiveBigIntegerField(default=0)
    existance_mesures_prevention_incendies = models.CharField(max_length=255, choices=OUI_NON_CHOICES)
    
    eclairage_existant = models.CharField(max_length=255, choices=OUI_NON_CHOICES)
    source_principale_energetique = models.CharField(max_length=255, null=True, blank=True)
    
    def __str__(self):
        return self.site.nom_site
    
class DetailsTypeAbrisProfilSiteSerializer(serializers.ModelSerializer):
    class Meta:
        model = DetailsTypeAbrisProfilSite
        fields = '__all__'
        
class AbrisAmesProfilSiteSerializer(serializers.ModelSerializer):
    details_types_abris = DetailsTypeAbrisProfilSiteSerializer(many=True)
    class Meta:
        model = AbrisAmesProfilSite
        fields = '__all__'
        
class CreateAbrisAmesProfilSiteSerializer(serializers.ModelSerializer):
    class Meta:
        model = AbrisAmesProfilSite
        fields = '__all__'
        
    def create(self, validated_data):
        details_types_abris = validated_data.pop('details_types_abris')
        abris_ames = AbrisAmesProfilSite.objects.create(**validated_data)
        for detail_type_abris in details_types_abris:
            detail = DetailsTypeAbrisProfilSite.objects.create(**detail_type_abris)
            abris_ames.details_types_abris.add(detail)
        return abris_ames