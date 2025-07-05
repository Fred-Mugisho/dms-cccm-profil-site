from django.db import models

class HistoriqueSynchro(models.Model):
    dernier_synchro = models.DateTimeField(auto_now_add=True, verbose_name="Dernier synchro")
    
    def __str__(self):
        return str(self.dernier_synchro)

class CoordonneesSite(models.Model):
    site_name = models.CharField(max_length=255, unique=True)
    type_site = models.CharField(max_length=50)
    url_map = models.URLField(null=True, blank=True)
    
    province = models.CharField(max_length=50, null=True, blank=True)
    territoire = models.CharField(max_length=50, null=True, blank=True)
    zone_sante = models.CharField(max_length=50, null=True, blank=True)
    coordinateur_site = models.CharField(max_length=50, null=True, blank=True)
    gestionnaire_site = models.CharField(max_length=50, null=True, blank=True)
    sous_mecanisme = models.BooleanField(default=False)
    
    nombre_menages = models.PositiveIntegerField(default=0)
    nombre_individus = models.PositiveIntegerField(default=0)
    latitude = models.FloatField()
    longitude = models.FloatField()
    
    def __str__(self):
        return self.site_name

class MouvementDeplace(models.Model):
    provenance = models.CharField(max_length=255)
    menage = models.PositiveIntegerField()
    individus = models.PositiveIntegerField()
    personne_vivant_handicape = models.PositiveIntegerField(default=0)
    
    typemouvement = models.CharField(max_length=50)
    raison = models.CharField(max_length=255)
    statutmouvement = models.CharField(max_length=50)
    
    individu_tranche_age_0_4_f = models.PositiveBigIntegerField(default=0)
    individu_tranche_age_5_11_f = models.PositiveBigIntegerField(default=0)
    individu_tranche_age_12_17_f = models.PositiveBigIntegerField(default=0)
    individu_tranche_age_18_24_f = models.PositiveBigIntegerField(default=0)
    individu_tranche_age_25_59_f = models.PositiveBigIntegerField(default=0)
    individu_tranche_age_60_f = models.PositiveBigIntegerField(default=0)
    individu_tranche_age_0_4_h = models.PositiveBigIntegerField(default=0)
    individu_tranche_age_5_11_h = models.PositiveBigIntegerField(default=0)
    individu_tranche_age_12_17_h = models.PositiveBigIntegerField(default=0)
    individu_tranche_age_18_24_h = models.PositiveBigIntegerField(default=0)
    individu_tranche_age_25_59_h = models.PositiveBigIntegerField(default=0)
    individu_tranche_age_60_h = models.PositiveBigIntegerField(default=0)
    
    province = models.CharField(max_length=50, null=True, blank=True)
    territoire = models.CharField(max_length=50, null=True, blank=True)
    zone_sante = models.CharField(max_length=50, null=True, blank=True)
    
    site = models.CharField(max_length=50, null=True, blank=True)
    type_site = models.CharField(max_length=50, null=True, blank=True)
    coordinateur_site = models.CharField(max_length=50, null=True, blank=True)
    gestionnaire_site = models.CharField(max_length=50, null=True, blank=True)
    sous_mecanisme = models.BooleanField(default=False)
    
    organisation = models.CharField(max_length=50, null=True, blank=True)
    activite = models.PositiveBigIntegerField(default=1)
    enqueteur = models.CharField(max_length=50, null=True, blank=True)
    date_enregistrement = models.DateField()
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return str(self.date_enregistrement)