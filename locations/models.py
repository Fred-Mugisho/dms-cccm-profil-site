from django.db import models
# from django.contrib.gis.db import models as gis_models

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
    
    @property
    def zones_sante(self):
        from .serializers import ZoneSanteSerializer
        zones = ZoneSante.objects.filter(province=self)
        return ZoneSanteSerializer(zones, many=True).data

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
    province = models.ForeignKey(Province, on_delete=models.CASCADE)
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
