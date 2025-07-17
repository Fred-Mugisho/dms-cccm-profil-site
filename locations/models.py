from django.db import models, transaction
# from django.contrib.gis.db import models as gis_models
import logging

# Administration divisions
class Province(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=255, unique=True)
    
    def save(self, *args, **kwargs):
        if not self.code:
            code = f"0{self.id}" if self.id < 10 else self.id
            self.code = f"CD{code}"
        super(Province, self).save(*args, **kwargs)
        
    @property
    def territoires(self):
        from .serializers import TerritoireSerializer
        terrs = Territoire.objects.filter(province=self)
        return TerritoireSerializer(terrs, many=True).data

class Territoire(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=255, unique=True)
    province = models.ForeignKey(Province, on_delete=models.CASCADE)
    
    def save(self, *args, **kwargs):
        if not self.code:
            code = f"0{self.id}" if self.id < 10 else self.id
            self.code = f"{self.province.code}T{code}"
        super(Territoire, self).save(*args, **kwargs)
        
    @property
    def secteurs(self):
        from .serializers import SecteurSerializer
        secs = Secteur.objects.filter(territoire=self)
        return SecteurSerializer(secs, many=True).data
    
    @property
    def zones_sante(self):
        from .serializers import ZoneSanteSerializer
        zones = ZoneSante.objects.filter(territoire=self)
        return ZoneSanteSerializer(zones, many=True).data

class Secteur(models.Model):  # Chefferie, secteur, ou commune
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=255, unique=True)
    territoire = models.ForeignKey(Territoire, on_delete=models.CASCADE)
    
    def save(self, *args, **kwargs):
        if not self.code:
            code = f"0{self.id}" if self.id < 10 else self.id
            self.code = f"{self.territoire.code}S{code}"
        super(Secteur, self).save(*args, **kwargs)
        
    @property
    def groupements(self):
        from .serializers import GroupementSerializer
        groups = Groupement.objects.filter(secteur=self)
        return GroupementSerializer(groups, many=True).data

class Groupement(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=255, unique=True)
    secteur = models.ForeignKey(Secteur, on_delete=models.CASCADE)
    
    def save(self, *args, **kwargs):
        if not self.code:
            code = f"0{self.id}" if self.id < 10 else self.id
            self.code = f"{self.secteur.code}G{code}"
        super(Groupement, self).save(*args, **kwargs)
        
    @property
    def villages(self):
        from .serializers import VillageSerializer
        vils = Village.objects.filter(groupement=self)
        return VillageSerializer(vils, many=True).data

class Village(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=255, unique=True)
    groupement = models.ForeignKey(Groupement, on_delete=models.CASCADE)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    
    def save(self, *args, **kwargs):
        if not self.code:
            code = f"0{self.id}" if self.id < 10 else self.id
            self.code = f"{self.groupement.code}V{code}"
        super(Village, self).save(*args, **kwargs)

# Santé
class ZoneSante(models.Model):  # Zone de santé
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=255, unique=True)
    territoire = models.ForeignKey(Territoire, on_delete=models.CASCADE)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    
    def save(self, *args, **kwargs):
        if not self.code:
            code = f"0{self.id}" if self.id < 10 else self.id
            self.code = f"{self.province.code}ZS{code}"
        super(ZoneSante, self).save(*args, **kwargs)
        
    @property
    def aires_sante(self):
        from .serializers import AireSanteSerializer
        aires = AireSante.objects.filter(health_zone=self)
        return AireSanteSerializer(aires, many=True).data

class AireSante(models.Model):  # Aire de santé
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=255, unique=True)
    health_zone = models.ForeignKey(ZoneSante, on_delete=models.CASCADE)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    
    def save(self, *args, **kwargs):
        if not self.code:
            code = f"0{self.id}" if self.id < 10 else self.id
            self.code = f"{self.health_zone.code}AS{code}"
        super(AireSante, self).save(*args, **kwargs)

class LimiteAdministrative(models.Model):
    LEVEL_CHOICES = [
        ('Province', 'Province'),
        ('territoire', 'Territoire'),
        ('secteur', 'Secteur'),
        ('groupement', 'Groupement'),
        ('village', 'Village'),
        # Santé
        ('Zone de santé', 'Zone de Santé'),
        ('Aire de santé', 'Aire de Santé'),
    ]

    name = models.CharField(max_length=255)
    code = models.CharField(max_length=30, unique=True)
    level = models.CharField(max_length=50, choices=LEVEL_CHOICES)
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='children')
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    limite = models.JSONField(null=True, blank=True)  # pour les polygones

    class Meta:
        verbose_name_plural = "LIMITES ADMINISTRATIVES"

    def __str__(self):
        return f"{self.name} ({self.level()})"
    
    @property
    def children(self):
        from .serializers import LimiteAdministrativeSerializer
        limites = LimiteAdministrative.objects.filter(parent=self)
        return LimiteAdministrativeSerializer(limites, many=True).data
    
class DataImport(models.Model):
    province = models.CharField(max_length=300, null=True, blank=True)
    code_province = models.CharField(max_length=300, null=True, blank=True)
    territoire = models.CharField(max_length=300, null=True, blank=True)
    code_territoire = models.CharField(max_length=300, null=True, blank=True)
    zone_sante = models.CharField(max_length=300, null=True, blank=True)
    code_zone_sante = models.CharField(max_length=300, null=True, blank=True)
    type_site = models.CharField(max_length=300, null=True, blank=True)
    longitude = models.DecimalField(decimal_places=6, max_digits=9, null=True, blank=True)
    latitude = models.DecimalField(decimal_places=6, max_digits=9, null=True, blank=True)
    
    code_site = models.CharField(max_length=300, null=True, blank=True)
    nom_site = models.CharField(max_length=300)
    
    type_mouvement = models.CharField(max_length=300, default="entree_initiale")
    menages = models.PositiveBigIntegerField(default=0)
    individus = models.PositiveBigIntegerField(default=0)
    
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
    date_mise_a_jour = models.DateField()
    
    def __str__(self):
        return self.nom_site
    
class TemporalDataImport(models.Model):
    province = models.CharField(max_length=300, null=True, blank=True)
    code_province = models.CharField(max_length=300, null=True, blank=True)
    territoire = models.CharField(max_length=300, null=True, blank=True)
    code_territoire = models.CharField(max_length=300, null=True, blank=True)
    zone_sante = models.CharField(max_length=300, null=True, blank=True)
    code_zone_sante = models.CharField(max_length=300, null=True, blank=True)
    type_site = models.CharField(max_length=300, null=True, blank=True)
    longitude = models.DecimalField(decimal_places=6, max_digits=9, null=True, blank=True)
    latitude = models.DecimalField(decimal_places=6, max_digits=9, null=True, blank=True)
    
    code_site = models.CharField(max_length=300, null=True, blank=True)
    nom_site = models.CharField(max_length=300)
    
    type_mouvement = models.CharField(max_length=300, default="data_import")
    menages = models.PositiveBigIntegerField(default=0)
    individus = models.PositiveBigIntegerField(default=0)
    date_mise_a_jour = models.DateField()
    
    def __str__(self):
        return self.nom_site
    
    def extract_demographic_data(self):
        pourc_hommes = {
            '0_4': 19.8,
            '5_11': 15.9,
            '12_17': 19.34,
            '18_24': 12.35,
            '25_59': 28.81,
            '60': 3.80,
        }

        pourc_femmes = {
            '0_4': 19.3,
            '5_11': 15.5,
            '12_17': 18.1,
            '18_24': 12.57,
            '25_59': 29.33,
            '60': 4.2,
        }

        if self.individus == 0:
            return {f'individus_{tranche}_{sexe}': 0 for tranche in pourc_hommes for sexe in ('f', 'h')}

        resultats_temp = []

        for tranche in pourc_hommes:
            pct_h = pourc_hommes[tranche]
            pct_f = pourc_femmes[tranche]
            total_pct = pct_h + pct_f

            total_tranche = self.individus * (total_pct / 200)
            nb_femmes = total_tranche * (pct_f / total_pct)
            nb_hommes = total_tranche * (pct_h / total_pct)

            resultats_temp.append((f'individus_{tranche}_f', nb_femmes))
            resultats_temp.append((f'individus_{tranche}_h', nb_hommes))

        resultats = {}
        total_arrondi = 0
        restes = []

        for cle, valeur in resultats_temp:
            arrondi = int(valeur)
            resultats[cle] = arrondi
            total_arrondi += arrondi
            restes.append((cle, valeur - arrondi))

        difference = self.individus - total_arrondi

        # Donner toutes les unités restantes à une seule tranche, celle avec le plus grand reste décimal
        if difference > 0:
            cle_cible, _ = max(restes, key=lambda x: x[1])
            resultats[cle_cible] += difference

        return resultats