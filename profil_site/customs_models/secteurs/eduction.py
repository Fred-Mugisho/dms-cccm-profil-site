from django.db import models
from data_import.models import SiteDeplace
from utils.choices import *
from ..bases.base_model import BaseModel
from rest_framework import serializers

class EducationProfilSite(BaseModel):
    site = models.ForeignKey(SiteDeplace, on_delete=models.CASCADE, db_index=True)
    existance_ecoles_primaire_fonctionnelles = models.CharField(max_length=255, choices=OUI_NON_CHOICES)
    distance_ecole_primaire_avec_site = models.PositiveBigIntegerField(default=0)
    existance_ecoles_secondaire_fonctionnelles = models.CharField(max_length=255, choices=OUI_NON_CHOICES)
    distance_ecole_secondaire_avec_site = models.PositiveBigIntegerField(default=0)
    nombre_enfants_en_age_scolaire_sont_scolarises = models.PositiveBigIntegerField(default=0)
    principales_obstacles_scolarisation = models.TextField(null=True, blank=True)
    activites_educatives_informelle_existantes = models.CharField(max_length=255, choices=OUI_NON_CHOICES)
    nb_enfants_age_scolaire_acces_educatives_informelles = models.PositiveBigIntegerField(default=0)
    
    def __str__(self):
        return self.site.nom_site
    
class EducationProfilSiteSerializer(serializers.ModelSerializer):
    class Meta:
        model = EducationProfilSite
        fields = '__all__'
        
class FormEducationProfilSiteSerializer(serializers.ModelSerializer):
    code_site = serializers.CharField(required=False)
    class Meta:
        model = EducationProfilSite
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
        
        gestion_admin = EducationProfilSite.objects.create(site=site, **validated_data)
        return gestion_admin