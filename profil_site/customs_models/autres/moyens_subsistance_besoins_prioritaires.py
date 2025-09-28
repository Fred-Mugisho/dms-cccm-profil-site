from django.db import models
from data_import.models import SiteDeplace
from utils.choices import *
from ..bases.base_model import BaseModel
from rest_framework import serializers

class MoyenSubsistanceBesoinPrioritaireProfilSite(BaseModel):
    site = models.ForeignKey(SiteDeplace, on_delete=models.CASCADE, db_index=True)
    marche_existant_interieur_site = models.CharField(max_length=255, choices=OUI_NON_CHOICES)
    distance_marche_avec_site = models.PositiveBigIntegerField(default=0)
    articles_necessaires_inexistantes_marche = models.TextField(null=True, blank=True)
    principaux_moyers_subsistance = models.TextField(null=True, blank=True)
    nombre_familles_gagnant_revenu_derniers_jours = models.PositiveBigIntegerField(default=0)
    nombre_jeunes_avec_travail = models.PositiveBigIntegerField(default=0)
    existance_enclos_betails = models.CharField(max_length=255, choices=OUI_NON_CHOICES)
    
    premier_besoin_prioritaire = models.CharField(max_length=255)
    deuxieme_besoin_prioritaire = models.CharField(max_length=255)
    troisieme_besoin_prioritaire = models.CharField(max_length=255)
    
    def __str__(self):
        return self.site.nom_site
    
class MoyenSubsistanceBesoinPrioritaireProfilSiteSerializer(serializers.ModelSerializer):
    class Meta:
        model = MoyenSubsistanceBesoinPrioritaireProfilSite
        fields = '__all__'
        
class FormMoyenSubsistanceBesoinPrioritaireProfilSiteSerializer(serializers.ModelSerializer):
    code_site = serializers.CharField(required=False)
    class Meta:
        model = MoyenSubsistanceBesoinPrioritaireProfilSite
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
        
        gestion_admin = MoyenSubsistanceBesoinPrioritaireProfilSite.objects.create(site=site, **validated_data)
        return gestion_admin