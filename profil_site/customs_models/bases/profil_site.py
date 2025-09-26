from data_import.models import SiteDeplace
from django.db import models
from rest_framework import serializers
from .base_model import BaseModel
from data_import.serializers import SiteDeplaceSerializer

class ProfilSite(BaseModel):
    site = models.ForeignKey(SiteDeplace, on_delete=models.CASCADE, db_index=True)
    enqueteur = models.CharField(max_length=255)
    organisation = models.CharField(max_length=255)
    concerne_nouveau_site = models.BooleanField(default=False)
    nombre_menages = models.PositiveBigIntegerField(default=0)
    nombre_individus = models.PositiveBigIntegerField(default=0)
    
    # Personnes par groupe d'age et sexe
    individus_0_4_f = models.PositiveBigIntegerField(default=0)
    individus_5_11_f = models.PositiveBigIntegerField(default=0)
    individus_12_17_f = models.PositiveBigIntegerField(default=0)
    individus_18_24_f = models.PositiveBigIntegerField(default=0)
    individus_25_59_f = models.PositiveBigIntegerField(default=0)
    individus_60_f = models.PositiveBigIntegerField(default=0)
    individus_0_4_h = models.PositiveBigIntegerField(default=0)
    individus_5_11_h = models.PositiveBigIntegerField(default=0)
    individus_12_17_h = models.PositiveBigIntegerField(default=0)
    individus_18_24_h = models.PositiveBigIntegerField(default=0)
    individus_25_59_h = models.PositiveBigIntegerField(default=0)
    individus_60_h = models.PositiveBigIntegerField(default=0)
    
    statut_site = models.CharField(max_length=255) # Fonctionnel ou non fonctionnel
    
    def __str__(self):
        return self.site.nom_site
    
class ProfilSiteSerializer(serializers.ModelSerializer):
    site = SiteDeplaceSerializer()
    class Meta:
        model = ProfilSite
        fields = '__all__'
        
class FormProfilSiteSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProfilSite
        fields = '__all__'