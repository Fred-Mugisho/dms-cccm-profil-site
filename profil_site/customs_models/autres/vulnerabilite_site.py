from ..bases.base_model import BaseModel
from django.db import models
from data_import.models import SiteDeplace
from rest_framework import serializers

class VulnerabilitePopulationProfilSite(BaseModel):
    site = models.ForeignKey(SiteDeplace, on_delete=models.CASCADE, db_index=True)
    nouvelle_arrivees_mois = models.PositiveBigIntegerField(default=0)
    retourneees_mois = models.PositiveBigIntegerField(default=0)
    raisons_retour = models.TextField(null=True, blank=True)
    
    menages_diriges_femmes = models.PositiveBigIntegerField(default=0)
    menages_diriges_enfants = models.PositiveBigIntegerField(default=0)
    enfants_non_accompagnes = models.PositiveBigIntegerField(default=0)
    personnes_handicaps_physiques = models.PositiveBigIntegerField(default=0)
    personnes_handicaps_mentaux = models.PositiveBigIntegerField(default=0)
    personnes_maladies_chroniques = models.PositiveBigIntegerField(default=0)
    personnes_agees_sans_membre = models.PositiveBigIntegerField(default=0) # Personne de 60 ans et plus, sans membre de la famille dans le pays d’accueil. La personne peut recevoir, ou pas, de l’assistance de la communauté.
    
    def __str__(self):
        return self.site.nom_site
    
class VulnerabilitePopulationProfilSiteSerializer(serializers.ModelSerializer):
    class Meta:
        model = VulnerabilitePopulationProfilSite
        fields = '__all__'