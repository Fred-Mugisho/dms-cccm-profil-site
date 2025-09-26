from django.db import models

from data_import.models import SiteDeplace
from utils.choices import *
from ..bases.base_model import BaseModel
from rest_framework import serializers

class ProtectionProfilSite(BaseModel):
    site = models.ForeignKey(SiteDeplace, on_delete=models.CASCADE, db_index=True)
    existance_restrictions_mouvement_interieur_exterieur = models.CharField(max_length=255, choices=OUI_NON_CHOICES)
    restrictions_mouvement_rencontrees = models.TextField(null=True, blank=True)
    tensions_entre_familles = models.CharField(max_length=255)
    incidents_securite_produits = models.CharField(max_length=255)
    acteurs_impliques_incidents_securite = models.TextField(null=True, blank=True)
    nature_incidents_securite = models.TextField(null=True, blank=True)
    personnes_sentiment_securite = models.CharField(max_length=255, choices=OUI_NON_CHOICES)
    menances_plus_courantes = models.TextField(null=True, blank=True)
    zones_insecurisees_femmes = models.TextField(null=True, blank=True)
    zones_insecurisees_hommes = models.TextField(null=True, blank=True)
    installantes_service_pvh_existantes = models.CharField(max_length=255, choices=OUI_NON_CHOICES)
    types_services_soutien_psychosocial = models.TextField(null=True, blank=True)
    nombres_familles_sans_documents_necessaires = models.PositiveBigIntegerField(default=0)
    distance_avec_bureaux_etat = models.PositiveBigIntegerField(default=0)
    accessibles_personnes_vulnerables = models.CharField(max_length=255, choices=OUI_NON_CHOICES)
    
    def __str__(self):
        return self.site.nom_site
    
class ProtectionProfilSiteSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProtectionProfilSite
        fields = '__all__'