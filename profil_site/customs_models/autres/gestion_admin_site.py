from data_import.models import SiteDeplace
from django.db import models
from rest_framework import serializers
from ..bases.base_model import BaseModel

class GestionAdminProfilSite(BaseModel):
    site = models.ForeignKey(SiteDeplace, on_delete=models.CASCADE, db_index=True)
    gestionnaire = models.CharField(max_length=300, null=True, blank=True)
    contact_gestionnaire = models.CharField(max_length=300, null=True, blank=True)
    administrateur = models.CharField(max_length=300, null=True, blank=True)
    contact_administrateur = models.CharField(max_length=300, null=True, blank=True)
    coordinateur = models.CharField(max_length=300, null=True, blank=True)
    contact_coordinateur = models.CharField(max_length=300, null=True, blank=True)
    
    def __str__(self):
        return self.site.nom_site
    
    
class GestionAdminProfilSiteSerializer(serializers.ModelSerializer):
    class Meta:
        model = GestionAdminProfilSite
        fields = '__all__'
