from ..bases.base_model import BaseModel
from django.db import models
from data_import.models import SiteDeplace
from utils.choices import *
from rest_framework import serializers
from django.db import transaction

class DetailsTypeAbrisProfilSite(BaseModel):
    type_abris = models.CharField(max_length=255)
    nombre_installes = models.PositiveBigIntegerField(default=0)
    nombre_occupees = models.PositiveBigIntegerField(default=0)
    nombre_occupees_maintenance = models.PositiveBigIntegerField(default=0)
    nombre_occupees_remplacement = models.PositiveBigIntegerField(default=0)
    
    def __str__(self):
        return self.type_abris

class AbrisAmesProfilSite(BaseModel):
    site = models.ForeignKey(SiteDeplace, on_delete=models.CASCADE, db_index=True)
    capacite_accueil_max = models.PositiveBigIntegerField(default=0)
    familles_attente_parcelle_abris = models.PositiveBigIntegerField(default=0)
    fermeture_site_prevue = models.CharField(max_length=255, choices=OUI_NON_CHOICES)
    
    types_abris_present = models.TextField() # Separator: ;
    nombre_abris_occupes_maintenance = models.PositiveBigIntegerField(default=0)
    nombre_abris_occupes_remplacement = models.PositiveBigIntegerField(default=0)
    details_types_abris = models.ManyToManyField(DetailsTypeAbrisProfilSite, blank=True)
    
    besoins_en_ames = models.TextField()
    besoins_ames_saison_seche = models.TextField()
    strategies_adaptation_ames = models.TextField()
    
    etat_generale_parcelle_communautaire = models.CharField(max_length=255)
    etat_generale_routes = models.CharField(max_length=255)
    etat_generale_canaux_evacuations_eaux_pluviales = models.CharField(max_length=255)
    inodations_derniers_saison = models.CharField(max_length=255, choices=OUI_NON_CHOICES)
    nombre_incendies_ce_mois = models.PositiveBigIntegerField(default=0)
    existance_mesures_prevention_incendies = models.CharField(max_length=255, choices=OUI_NON_CHOICES)
    
    eclairage_existant = models.CharField(max_length=255, choices=OUI_NON_CHOICES)
    source_principale_energetique = models.CharField(max_length=255, null=True, blank=True)
    
    def __str__(self):
        return self.site.nom_site
    
class DetailsTypeAbrisProfilSiteSerializer(serializers.ModelSerializer):
    class Meta:
        model = DetailsTypeAbrisProfilSite
        fields = '__all__'
        
class AbrisAmesProfilSiteSerializer(serializers.ModelSerializer):
    details_types_abris = DetailsTypeAbrisProfilSiteSerializer(many=True)
    class Meta:
        model = AbrisAmesProfilSite
        fields = '__all__'
        
class FormAbrisAmesProfilSiteSerializer(serializers.ModelSerializer):
    code_site = serializers.CharField(required=False)
    details_types_abris = DetailsTypeAbrisProfilSiteSerializer(many=True)

    class Meta:
        model = AbrisAmesProfilSite
        fields = '__all__'
        extra_kwargs = {
            'site': {'read_only': True},
        }

    def create(self, validated_data):
        with transaction.atomic():
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

            # On récupère les détails imbriqués
            details_types_abris_data = validated_data.pop('details_types_abris', [])

            # Création de AbrisAmes
            abris_ames = AbrisAmesProfilSite.objects.create(site=site, **validated_data)

            # Création des détails
            details_instances = []
            for detail_data in details_types_abris_data:
                detail = DetailsTypeAbrisProfilSite.objects.create(**detail_data)
                details_instances.append(detail)

            # Liaison ManyToMany
            abris_ames.details_types_abris.set(details_instances)

            return abris_ames
