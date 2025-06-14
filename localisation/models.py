from django.db import models

class Position(models.Model):
    latitude = models.DecimalField(max_digits=9, decimal_places=6, verbose_name="Latitude")
    longitude = models.DecimalField(max_digits=9, decimal_places=6, verbose_name="Longitude")
    altitude = models.FloatField(null=True, blank=True, verbose_name="Altitude")
    precision = models.FloatField(null=True, blank=True, verbose_name="Précision (m)")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Date de création")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Date de mise à jour")
    
    class Meta:
        verbose_name = "Position"
        verbose_name_plural = "Positions"

    def __str__(self):
        return f"{self.latitude}, {self.longitude}"

class Localisation(models.Model):
    TYPE_CHOICES = [
        ("pays", "Pays"),
        ("province", "Province"),
        ("territoire", "Territoire"),
        ("ville", "Ville"),
        ("commune", "Commune"),
        ("secteur", "Secteur"),
        ("groupement", "Groupement"),
        ("quartier", "Quartier"),
        ("avenue", "Avenue"),
        ("village", "Village"),
        ("zone", "Zone de Santé"),
        ("aire", "Aire de Santé"),
    ]

    type = models.CharField(max_length=30, choices=TYPE_CHOICES, default="pays", verbose_name="Type")
    nom = models.CharField(max_length=200, verbose_name="Nom")
    code = models.CharField(max_length=200, unique=True, blank=True, null=True, verbose_name="Code")
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='enfants')
    position = models.OneToOneField(Position, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Date de création")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Date de mise à jour")

    class Meta:
        verbose_name = "Localisation"
        verbose_name_plural = "Localisations"
        unique_together = ('type', 'nom')
        
    def save(self, *args, **kwargs):
        if not self.code:
            self.code = self.generate_code()
        super(Localisation, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.nom} ({self.type})"
    
    def generate_code(self):
        # Gérer les codes en fonction du type
        localisations_type = Localisation.objects.filter(type=self.type).exclude(id=self.id)
        if localisations_type.exists():
            num = localisations_type.count() + 1
        else:
            num = 1
        
        numero = f"{num}"
        if num < 10:
            numero = f"00{num}"
        elif num < 100:
            numero = f"0{num}"
            
        if self.type == "pays":
            return "CD"
        elif self.type == "province":
            return f"CD{numero}"
        elif self.type == "territoire":
            return f"{self.parent.code}T{numero}"
        elif self.type == "ville":
            return f"{self.parent.code}V{numero}"
        elif self.type == "commune":
            return f"{self.parent.code}C{numero}"
        elif self.type == "secteur":
            return f"{self.parent.code}S{numero}"
        elif self.type == "groupement":
            return f"{self.parent.code}G{numero}"
        elif self.type == "quartier":
            return f"{self.parent.code}Q{numero}"
        elif self.type == "avenue":
            return f"{self.parent.code}A{numero}"
        elif self.type == "village":
            return f"{self.parent.code}V{numero}"
        elif self.type == "zone":
            return f"{self.parent.code}Z{numero}"
        elif self.type == "aire":
            return f"{self.parent.code}A{numero}"
