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
        
class FormGestionAdminProfilSiteSerializer(serializers.ModelSerializer):
    code_site = serializers.CharField(required=False)
    class Meta:
        model = GestionAdminProfilSite
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
        
        gestion_admin = GestionAdminProfilSite.objects.create(site=site, **validated_data)
        return gestion_admin
