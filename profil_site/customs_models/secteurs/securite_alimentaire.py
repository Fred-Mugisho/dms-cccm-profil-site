from ..bases.base_model import BaseModel
from django.db import models
from data_import.models import SiteDeplace
from utils.choices import *
from rest_framework import serializers

class SecuriteAlimentaireProfilSite(BaseModel):
    site = models.ForeignKey(SiteDeplace, on_delete=models.CASCADE, db_index=True)
    repas_par_jour_familles = models.PositiveBigIntegerField(default=0)
    difficultes_rencontrees_acces_nourriture = models.TextField(null=True, blank=True)
    existance_magasins_stockages_vivres = models.CharField(max_length=255, choices=OUI_NON_CHOICES)
    regularite_aide_alimentaire_derniers_mois = models.CharField(max_length=255)
    
    def __str__(self):
        return self.site.nom_site
    
class SecuriteAlimentaireProfilSiteSerializer(serializers.ModelSerializer):
    class Meta:
        model = SecuriteAlimentaireProfilSite
        fields = '__all__'
        
class FormSecuriteAlimentaireProfilSiteSerializer(serializers.ModelSerializer):
    code_site = serializers.CharField(required=False)
    class Meta:
        model = SecuriteAlimentaireProfilSite
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
        
        gestion_admin = SecuriteAlimentaireProfilSite.objects.create(site=site, **validated_data)
        return gestion_admin