from django.db import models
from utils.choices import *

class InformationGeneraleProfilSite(models.Model):
    siteId = models.PositiveBigIntegerField()
    nom_site = models.CharField(max_length=255, null=True, blank=True)
    code_enqueteur = models.CharField(max_length=255, null=True, blank=True)
    gestionnaireId = models.PositiveBigIntegerField()
    nom_gestionnaire = models.CharField(max_length=255, null=True, blank=True)
    coordinateurId = models.PositiveBigIntegerField()
    nom_coordinateur = models.CharField(max_length=255, null=True, blank=True)
    nb_menages = models.PositiveIntegerField()
    nb_individus = models.PositiveIntegerField()
    latitude = models.FloatField()
    longitude = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "INFORMATION GENERALE"
        verbose_name_plural = "INFORMATIONS GENERALES"

    def __str__(self):
        return self.nom_site
    
    @property
    def get_site(self):
        return None
    
    @property
    def get_gestionnaire(self):
        return None
    
    @property
    def get_coordinateur(self):
        return None
    
    @property
    def autres_data(self):
        from .serializers import GestionSiteSerializer, WashSiteSerializer, SanteSiteSerializer
        gestion_site = GestionSite.objects.filter(profil=self).first()
        wash_site = WashSite.objects.filter(profil=self).first()
        sante_site = SanteSite.objects.filter(profil=self).first()
        
        gestion_site_serializer = GestionSiteSerializer(gestion_site).data if gestion_site else None
        wash_site_serializer = WashSiteSerializer(wash_site).data if wash_site else None
        sante_site_serializer = SanteSiteSerializer(sante_site).data if sante_site else None
        
        return {
            "gestion_site": gestion_site_serializer,
            "wash_site": wash_site_serializer,
            "sante_site": sante_site_serializer
        }
    
class GestionSite(models.Model):
    profil = models.OneToOneField(InformationGeneraleProfilSite, on_delete=models.CASCADE, related_name="gestion_site")
    bureau_dedie = models.CharField(max_length=255, choices=OUI_NON_CHOICES, default="Non")
    nb_hommes_gestion = models.PositiveIntegerField()
    nb_femmes_gestion = models.PositiveIntegerField()
    comites_present = models.CharField(max_length=255, choices=OUI_NON_CHOICES, default="Non")
    comites_eliges_par_population = models.CharField(max_length=255, choices=OUI_NON_CHOICES, default="Non")
    comites_formes = models.CharField(max_length=255, choices=OUI_NON_CHOICES, default="Non")
    reunions_organisees = models.CharField(max_length=255, choices=OUI_NON_CHOICES, default="Non")
    comites_representatifs = models.CharField(max_length=255, choices=OUI_NON_CHOICES, default="Non")
    comites_gestion = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "GESTION DU SITE"
        verbose_name_plural = "GESTION DES SITES"
    
    def __str__(self):
        return self.profil.nom_site
    
class WashSite(models.Model):
    profil = models.OneToOneField(InformationGeneraleProfilSite, on_delete=models.CASCADE, related_name="wash_site")
    qte_eau_litres_par_personne = models.FloatField()
    source_principale_eau = models.CharField(max_length=255, choices=SOURCE_EAU_CHOICES)
    signes_defecation_air_libre = models.CharField(max_length=255, choices=OUI_NON_CHOICES, default="Non")
    jours_sans_eau_potable = models.PositiveIntegerField()
    savon_disponible = models.CharField(max_length=255, choices=OUI_NON_CHOICES, default="Non")
    inondations_dommages = models.CharField(max_length=255, choices=OUI_NON_CHOICES, default="Non")
    methode_elimination_dechets = models.CharField(max_length=255, choices=ELIMINATION_DECHETS_CHOICES)
    types_latrines_fonctionnelles = models.TextField(null=True, blank=True)
    types_douches_fonctionnelles = models.TextField(null=True, blank=True)
    douches_separees = models.CharField(max_length=255, choices=OUI_NON_CHOICES, default="Non")
    latrines_vidangees = models.CharField(max_length=255, choices=OUI_NON_CHOICES, default="Non")
    date_derniere_vidange = models.DateField(null=True, blank=True)
    eclairage_latrines_douches = models.CharField(max_length=255, choices=OUI_NON_CHOICES, default="Non")
    installation_adaptees_handicapes = models.CharField(max_length=255, choices=OUI_NON_CHOICES, default="Non")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "WASH DU SITE"
        verbose_name_plural = "WASH DES SITES"
    
    def __str__(self):
        return self.profil.nom_site
    
class SanteSite(models.Model):
    profil = models.OneToOneField(InformationGeneraleProfilSite, on_delete=models.CASCADE, related_name="sante_site")
    prestataire_disponible = models.CharField(max_length=255, choices=OUI_NON_CHOICES, default="Non")
    prestataire_dans_site = models.CharField(max_length=255, choices=OUI_NON_CHOICES, default="Non")
    service_urgence = models.CharField(max_length=255, choices=OUI_NON_CHOICES, default="Non")
    service_chirurgie = models.CharField(max_length=255, choices=OUI_NON_CHOICES, default="Non")
    service_pediatrie = models.CharField(max_length=255, choices=OUI_NON_CHOICES, default="Non")
    service_prenatal = models.CharField(max_length=255, choices=OUI_NON_CHOICES, default="Non")
    enfants_non_vaccines = models.PositiveBigIntegerField(default=0)
    problemes_sante = models.TextField(null=True, blank=True)
    obsacles_acces = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "SANTE DU SITE"
        verbose_name_plural = "SANTE DES SITES"
        
    def __str__(self):
        return self.profil.nom_site