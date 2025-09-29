from django.db import models

from data_import.models import SiteDeplace
from utils.choices import *
from ..bases.base_model import BaseModel
from rest_framework import serializers

class ProtectionProfilSite(BaseModel):
    site = models.ForeignKey(SiteDeplace, on_delete=models.CASCADE, db_index=True)
    existance_restrictions_mouvement_interieur_exterieur = models.CharField(max_length=255, choices=OUI_NON_CHOICES)
    restrictions_mouvement_rencontrees = models.TextField(null=True, blank=True)
    tensions_entre_familles = models.CharField(max_length=255) # OUI_NON_JE_PREFERE_NON_REPONDRE
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
        
class FormProtectionProfilSiteSerializer(serializers.ModelSerializer):
    code_site = serializers.CharField(required=False)
    class Meta:
        model = ProtectionProfilSite
        fields = '__all__'
        extra_kwargs = {
            'site': {'read_only': True}
        }
        
    def create(self, validated_data):
        code_site = validated_data.pop('code_site', None)
        if not code_site:
            raise serializers.ValidationError({
                "code_site": "Le code du site est obligatoire."
            })
            
        site = SiteDeplace.objects.filter(code_site=code_site).first()
        if not site:
            raise serializers.ValidationError({
                "code_site": f"Aucun site trouvé avec le code '{code_site}'."
            })
        
        gestion_admin = ProtectionProfilSite.objects.create(site=site, **validated_data)
        return gestion_admin