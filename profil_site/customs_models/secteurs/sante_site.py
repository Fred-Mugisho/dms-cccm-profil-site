from ..bases.base_model import BaseModel
from django.db import models
from data_import.models import SiteDeplace
from utils.choices import *
from rest_framework import serializers

class SanteProfilSite(BaseModel):
    site = models.ForeignKey(SiteDeplace, on_delete=models.CASCADE, db_index=True)
    problemes_sante = models.TextField()
    prestataire_sante_disponible = models.CharField(max_length=255, choices=OUI_NON_CHOICES)
    prestataire_sante_dans_site = models.CharField(max_length=255, choices=OUI_NON_CHOICES)
    distance_prestataire = models.PositiveBigIntegerField(default=0) # En km, Si le prestataire n'est pas dans le site
    service_urgence = models.CharField(max_length=255, choices=OUI_NON_CHOICES)
    service_chirurgie = models.CharField(max_length=255, choices=OUI_NON_CHOICES)
    service_pediatrie = models.CharField(max_length=255, choices=OUI_NON_CHOICES)
    service_prenatal = models.CharField(max_length=255, choices=OUI_NON_CHOICES)
    fournit_ambulance = models.CharField(max_length=255, choices=OUI_NON_CHOICES)
    problemes_familles_acceder_soins = models.TextField(null=True, blank=True)
    enfants_non_vaccines = models.PositiveBigIntegerField(default=0)
    
    def __str__(self):
        return self.site.nom_site
    
class SanteProfilSiteSerializer(serializers.ModelSerializer):
    class Meta:
        model = SanteProfilSite
        fields = '__all__'
        
class FormSanteProfilSiteSerializer(serializers.ModelSerializer):
    code_site = serializers.CharField(required=False)
    class Meta:
        model = SanteProfilSite
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
        
        gestion_admin = SanteProfilSite.objects.create(site=site, **validated_data)
        return gestion_admin