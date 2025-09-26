from ..bases.base_model import BaseModel
from django.db import models
from data_import.models import SiteDeplace
from utils.choices import *
from rest_framework import serializers

class WashProfilSite(BaseModel):
    site = models.ForeignKey(SiteDeplace, on_delete=models.CASCADE, db_index=True)
    nombre_litres_personne_jour = models.PositiveBigIntegerField(default=0)
    principale_source_eau_potable = models.TextField()
    source_principale_eau_potable_acceptable = models.CharField(max_length=255, choices=OUI_NON_CHOICES)
    nombre_moyen_jours_sans_eau_potable = models.PositiveBigIntegerField(default=0)
    signes_defecation_plein_air = models.CharField(max_length=255, choices=OUI_NON_CHOICES)
    savon_generalement_disponible = models.CharField(max_length=255, choices=OUI_NON_CHOICES)
    inondations_dommages = models.CharField(max_length=255, choices=OUI_NON_CHOICES)
    methode_elimination_dechets = models.CharField(max_length=255, choices=ELIMINATION_DECHETS_CHOICES)
    types_latrines_fonctionnelles = models.TextField(null=True, blank=True)
    nombre_latrines_fonctionnelles = models.PositiveBigIntegerField(default=0)
    types_douches_fonctionnelles = models.TextField(null=True, blank=True)
    nombre_douches_fonctionnelles = models.PositiveBigIntegerField(default=0)
    douches_separees = models.CharField(max_length=255, choices=OUI_NON_CHOICES)
    latrines_vidangees = models.CharField(max_length=255, choices=OUI_NON_CHOICES)
    date_derniere_vidange = models.DateField(null=True, blank=True)
    eclairage_latrines_douches = models.CharField(max_length=255, choices=OUI_NON_CHOICES)
    installation_adaptees_handicapes = models.CharField(max_length=255, choices=OUI_NON_CHOICES)
    
    def __str__(self):
        return self.site.nom_site
    
class WashProfilSiteSerializer(serializers.ModelSerializer):
    class Meta:
        model = WashProfilSite
        fields = '__all__'