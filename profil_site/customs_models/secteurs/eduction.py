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
    nombre_enfants_en_age_scolaire_accedent_activites_educatives_informelles = models.PositiveBigIntegerField(default=0)
    
    def __str__(self):
        return self.site.nom_site
    
class EducationProfilSiteSerializer(serializers.ModelSerializer):
    class Meta:
        model = EducationProfilSite
        fields = '__all__'