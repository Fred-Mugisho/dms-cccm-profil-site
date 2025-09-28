from django.db import models
from data_import.models import SiteDeplace
from utils.choices import *
from ..bases.base_model import BaseModel
from rest_framework import serializers

class CartographieServiceActeurProfilSite(BaseModel):
    site = models.ForeignKey(SiteDeplace, on_delete=models.CASCADE, db_index=True)
    
    # Accès aux services (Adequat, Inadequat, Inexistant)
    service_education = models.CharField(max_length=255)
    distribution_vivres = models.CharField(max_length=255)
    service_sante = models.CharField(max_length=255)
    service_sante_mental_psychosocial = models.CharField(max_length=255)
    service_moyen_existance = models.CharField(max_length=255)
    distribution_cash = models.CharField(max_length=255)
    distribution_nfi_ame = models.CharField(max_length=255)
    service_protection = models.CharField(max_length=255)
    service_maintenace_abris = models.CharField(max_length=255)
    service_wash = models.CharField(max_length=255)
    service_elimination_dechets = models.CharField(max_length=255)
    
    # Cartographie des acteurs
    existance_partenaires_protection = models.CharField(max_length=255, choices=OUI_NON_CHOICES)
    noms_partenaires_protection = models.TextField(null=True, blank=True)
    existance_partenaires_vbg = models.CharField(max_length=255, choices=OUI_NON_CHOICES)
    noms_partenaires_vbg = models.TextField(null=True, blank=True)
    existance_partenaires_protection_enfants = models.CharField(max_length=255, choices=OUI_NON_CHOICES)
    noms_partenaires_protection_enfants = models.TextField(null=True, blank=True)
    existance_partenaires_education = models.CharField(max_length=255, choices=OUI_NON_CHOICES)
    noms_partenaires_education = models.TextField(null=True, blank=True)
    existance_partenaires_abris_ame = models.CharField(max_length=255, choices=OUI_NON_CHOICES)
    noms_partenaires_abris_ame = models.TextField(null=True, blank=True)
    existance_partenaires_sante_eau = models.CharField(max_length=255, choices=OUI_NON_CHOICES)
    noms_partenaires_sante_eau = models.TextField(null=True, blank=True)
    existance_partenaires_assainissement = models.CharField(max_length=255, choices=OUI_NON_CHOICES)
    noms_partenaires_assainissement = models.TextField(null=True, blank=True)
    existance_partenaires_dechets = models.CharField(max_length=255, choices=OUI_NON_CHOICES)
    noms_partenaires_dechets = models.TextField(null=True, blank=True)
    existance_partenaires_santes_primaires = models.CharField(max_length=255, choices=OUI_NON_CHOICES)
    noms_partenaires_santes_primaires = models.TextField(null=True, blank=True)
    existance_partenaires_sante_secondaires = models.CharField(max_length=255, choices=OUI_NON_CHOICES)
    noms_partenaires_sante_secondaires = models.TextField(null=True, blank=True)
    existance_partenaires_sante_mental_psychosociaux = models.CharField(max_length=255, choices=OUI_NON_CHOICES)
    noms_partenaires_sante_mental_psychosociaux = models.TextField(null=True, blank=True)
    existance_partenaires_nutrition = models.CharField(max_length=255, choices=OUI_NON_CHOICES)
    noms_partenaires_nutrition = models.TextField(null=True, blank=True)
    existance_partenaires_securite_alimentaire = models.CharField(max_length=255, choices=OUI_NON_CHOICES)
    noms_partenaires_securite_alimentaire = models.TextField(null=True, blank=True)
    existance_partenaires_cohension_sociale = models.CharField(max_length=255, choices=OUI_NON_CHOICES)
    noms_partenaires_cohension_sociale = models.TextField(null=True, blank=True)
    existance_partenaires_moyens_subsistance = models.CharField(max_length=255, choices=OUI_NON_CHOICES)
    noms_partenaires_moyens_subsistance = models.TextField(null=True, blank=True)
    existance_partenaires_communication = models.CharField(max_length=255, choices=OUI_NON_CHOICES)
    noms_partenaires_communication = models.TextField(null=True, blank=True)
    
    def __str__(self):
        return self.site.nom_site
    
class CartographieServiceActeurProfilSiteSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartographieServiceActeurProfilSite
        fields = '__all__'
        
class FormCartographieServiceActeurProfilSiteSerializer(serializers.ModelSerializer):
    code_site = serializers.CharField(required=False)
    class Meta:
        model = CartographieServiceActeurProfilSite
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
        
        gestion_admin = CartographieServiceActeurProfilSite.objects.create(site=site, **validated_data)
        return gestion_admin