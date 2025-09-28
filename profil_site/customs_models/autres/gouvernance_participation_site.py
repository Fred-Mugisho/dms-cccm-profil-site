from ..bases.base_model import BaseModel
from django.db import models
from data_import.models import SiteDeplace
from utils.choices import *
from rest_framework import serializers

class OrganisationInterneFonctionnementProfilSite(BaseModel):
    site = models.ForeignKey(SiteDeplace, on_delete=models.CASCADE, db_index=True)
    bureau_dedie = models.CharField(max_length=255, choices=OUI_NON_CHOICES)
    nb_hommes_gestion = models.PositiveIntegerField(default=0)
    nb_femmes_gestion = models.PositiveIntegerField(default=0)
    comites_present = models.CharField(max_length=255, choices=OUI_NON_CHOICES)
    comites_gestion = models.TextField(null=True, blank=True)
    comites_eliges_par_population = models.CharField(max_length=255, choices=OUI_NON_CHOICES)
    comites_fonctionne = models.CharField(max_length=255, choices=COMITES_FONCTIONNELS_CHOICES)
    nb_comites_fonctionnels = models.PositiveIntegerField(default=0) # Si comites_fonctionne = Partiellement
    comites_formes = models.CharField(max_length=255, choices=OUI_NON_PARTIELLEMENT_CHOICES)
    reunions_organisees = models.CharField(max_length=255, choices=OUI_NON_CHOICES)
    comites_representatifs = models.CharField(max_length=255, choices=OUI_NON_CHOICES)
    nom_equipe_mobile_gestion = models.CharField(max_length=255, null=True, blank=True)
    
    methodes_annonce_distribution = models.TextField(null=True, blank=True)
    centre_communautaire = models.CharField(max_length=255, choices=OUI_NON_CHOICES)
    mecanisme_gestion_plainte = models.CharField(max_length=255, choices=OUI_NON_CHOICES)
    rencontres_coordination = models.CharField(max_length=255, choices=OUI_NON_CHOICES)
    rencontres_planification = models.CharField(max_length=255, choices=RENCONTRES_PLANIFICATION_CHOICES)
    
    def __str__(self):
        return self.site.nom_site
    
class OrganisationInterneFonctionnementProfilSiteSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrganisationInterneFonctionnementProfilSite
        fields = '__all__'
        
class FormOrganisationInterneFonctionnementProfilSiteSerializer(serializers.ModelSerializer):
    code_site = serializers.CharField(required=False)
    class Meta:
        model = OrganisationInterneFonctionnementProfilSite
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
        
        gestion_admin = OrganisationInterneFonctionnementProfilSite.objects.create(site=site, **validated_data)
        return gestion_admin