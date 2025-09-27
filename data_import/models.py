from django.db import models
from django.contrib.auth.models import User
import re


# NOUVELLE REFLEXION
class SiteDeplace(models.Model):
    province = models.CharField(max_length=300, null=True, blank=True, db_index=True)
    code_province = models.CharField(max_length=300, null=True, blank=True, db_index=True)
    territoire = models.CharField(max_length=300, null=True, blank=True, db_index=True)
    code_territoire = models.CharField(max_length=300, null=True, blank=True, db_index=True)
    zone_sante = models.CharField(max_length=300, null=True, blank=True, db_index=True)
    code_zone_sante = models.CharField(max_length=300, null=True, blank=True, db_index=True)
    type_site = models.CharField(max_length=300, null=True, blank=True, db_index=True)
    longitude = models.DecimalField(
        decimal_places=6, max_digits=9, null=True, blank=True
    )
    latitude = models.DecimalField(
        decimal_places=6, max_digits=9, null=True, blank=True
    )
    type_propriete_fonciere = models.CharField(max_length=300, null=True, blank=True, db_index=True)

    code_site = models.CharField(max_length=300, null=True, blank=True, db_index=True)
    nom_site = models.CharField(max_length=300, db_index=True)
    sous_mecanisme = models.BooleanField(default=True, db_index=True)
    gestionnaire = models.CharField(max_length=300, null=True, blank=True, db_index=True)
    coordinateur = models.CharField(max_length=300, null=True, blank=True, db_index=True)

    def __str__(self):
        return self.nom_site
    
    def save(self, *args, **kwargs):
        if not self.code_site:
            self.code_site = self.generate_code_new_site()
        super(SiteDeplace, self).save(*args, **kwargs)
        
    @staticmethod
    def extract_numero_site(code: str) -> int:
        """
        Extrait le numéro du site dans un code_site du type ...SNNN...[SP/CC/SS].
        Exemple: CD6102ZS01S003SPHM -> 3
                CD6102ZS01S1902SPHM -> 1902
        """
        match = re.search(r"S(\d+)(?=SP|CC|SS)", code)
        return int(match.group(1)) if match else 0
    
    def generate_code_new_site(self) -> str:
        """
        Génère un nouveau code_site en prenant le plus grand numéro existant
        et en incrémentant dessus.
        """
        codes_sites = SiteDeplace.objects.values_list("code_site", flat=True)

        if not codes_sites:
            numero = 1
        else:
            numeros = [self.extract_numero_site(code) for code in codes_sites if code]
            numero = (max(numeros) if numeros else 0) + 1

        return self.generate_code_site(order=numero)
        
    
    def generate_code_site(self, order: int, use_administratif: bool = False):
        """
        Génère le code complet du site selon le format officiel.

        Args:
            order: numéro du site (1..999)
            use_administratif: True pour format administratif, False pour format sanitaire

        Returns:
            str: code site complet
        """
        # SNNN : toujours 3 chiffres
        s_number = f"S{order:03d}"

        # Type de site : SP, CC ou SS
        site_type_map = {
            "Site Planifié": "SP",
            "SITE SPONTANÉ": "SP",
            "Centre Collectif": "CC",
            "SITE COLLECTIF": "CC",
            "Site Spontané": "SS",
            "SITE SPONTANÉ": "SS",
        }
        site_type = site_type_map.get(self.type_site, "SP")  # valeur par défaut SP si non trouvé

        # Gestion : SM ou HM
        gestion_type = "SM" if self.sous_mecanisme else "HM"

        if use_administratif:
            # Format administratif : CDXXTYYSZZGAASNNN[SP/CC/SS][SM/HM]
            code_site = f"{self.code_zone_sante}{s_number}{site_type}{gestion_type}"
        else:
            # Format sanitaire/humanitaire : CDXXTYYZSQQSNNN[SP/CC/SS][SM/HM]
            code_site = f"{self.code_zone_sante}{s_number}{site_type}{gestion_type}"

        ts = self.type_site.lower()
        self.code_site = code_site
        self.type_site = ts.title()
        # self.save(update_fields=["code_site", "type_site"])


    def deltas_menages_individus_type_mouvement(self, menages: int, individus: int):
        mouvements_site = MouvementDeplace.objects.filter(site=self)
        if not mouvements_site.exists():
            return menages, individus, "entree"

        actual_menages = 0
        actual_individus = 0
        for mouvement in mouvements_site:
            actual_menages += mouvement.menages
            actual_individus += mouvement.individus

        delta_menages = menages - actual_menages
        delta_individus = individus - actual_individus
        type_mouvement = "entree" if delta_individus >= 0 else "sortie"

        return abs(delta_menages), abs(delta_individus), type_mouvement

    def total_cumule_menages_individus(self):
        mouvements_site = MouvementDeplace.objects.filter(site=self)
        total_menages = 0
        total_individus = 0

        for m in mouvements_site:
            signe = 1 if m.type_mouvement == "entree" else -1
            total_menages += signe * abs(m.menages)
            total_individus += signe * abs(m.individus)

        return total_menages, total_individus

    def mouvements_temporaire(self):
        try:
            return TemporalMouvementDeplace.objects.filter(site=self).order_by(
                "date_mise_a_jour"
            )
        except TemporalMouvementDeplace.DoesNotExist:
            return []


class TemporalMouvementDeplace(models.Model):
    site = models.ForeignKey(SiteDeplace, on_delete=models.CASCADE)
    menages = models.PositiveBigIntegerField(default=0)
    individus = models.PositiveBigIntegerField(default=0)
    pvh = models.PositiveBigIntegerField(default=0)
    date_mise_a_jour = models.DateField()

    def __str__(self):
        return str(self.site.nom_site)


class MouvementDeplace(models.Model):
    site = models.ForeignKey(SiteDeplace, on_delete=models.CASCADE)
    menages = models.PositiveBigIntegerField(default=0)
    individus = models.PositiveBigIntegerField(default=0)
    type_mouvement = models.CharField(max_length=300, default="entree_initiale")

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

    pvh = models.PositiveBigIntegerField(default=0)

    date_mise_a_jour = models.DateField()

    def __str__(self):
        return str(self.site.nom_site)

    def total_cumule_menages_individus(self):
        mouvements_site = MouvementDeplace.objects.filter(site=self)
        total_menages = 0
        total_individus = 0

        for m in mouvements_site:
            signe = 1 if m.type_mouvement == "entree" else -1
            total_menages += signe * abs(m.menages)
            total_individus += signe * abs(m.individus)

        return total_menages, total_individus

    def extract_demographic_data(self):
        pourc_hommes = {
            "0_4": 19.8,
            "5_11": 15.9,
            "12_17": 19.34,
            "18_24": 12.35,
            "25_59": 28.81,
            "60": 3.80,
        }

        pourc_femmes = {
            "0_4": 19.3,
            "5_11": 15.5,
            "12_17": 18.1,
            "18_24": 12.57,
            "25_59": 29.33,
            "60": 4.2,
        }

        if self.individus == 0:
            return {
                f"individus_{tranche}_{sexe}": 0
                for tranche in pourc_hommes
                for sexe in ("f", "h")
            }

        resultats_temp = []

        for tranche in pourc_hommes:
            pct_h = pourc_hommes[tranche]
            pct_f = pourc_femmes[tranche]
            total_pct = pct_h + pct_f

            total_tranche = self.individus * (total_pct / 200)
            nb_femmes = total_tranche * (pct_f / total_pct)
            nb_hommes = total_tranche * (pct_h / total_pct)

            resultats_temp.append((f"individus_{tranche}_f", nb_femmes))
            resultats_temp.append((f"individus_{tranche}_h", nb_hommes))

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

    def save_democraphic_data(self):
        data = self.extract_demographic_data()
        for cle, valeur in data.items():
            setattr(self, cle, valeur)
        self.save()


class SiteUnique(models.Model):
    nom = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return self.nom


class MouvementDeplaceSiteUnique(models.Model):
    MOIS_CHOICE = [
        ("Mai2023", "Mai 2023"),
        ("Juin2023", "Juin 2023"),
        ("Juillet2023", "Juillet 2023"),
        ("Aout2023", "Aout 2023"),
        ("Sept2023", "Septembre 2023"),
        ("Oct2023", "Octobre 2023"),
        ("Nov2023", "Novembre 2023"),
        ("Dec2023", "Decembre 2023"),
        ("Janv2024", "Janvier 2024"),
        ("Fev2024", "Fevrier 2024"),
        ("Mars2024", "Mars 2024"),
        ("Avril2024", "Avril 2024"),
        ("Mai2024", "Mai 2024"),
        ("Juin2024", "Juin 2024"),
        ("Juillet2024", "Juillet 2024"),
        ("Aout2024", "Aout 2024"),
        ("Sept2024", "Septemembre 2024"),
        ("Oct2024", "Octobre 2024"),
        ("Nov2024", "Novembre 2024"),
        ("Janv2025", "Janvier 2025"),
        ("Fev2025", "Fevrier 2025"),
        ("Mars2025", "Mars 2025"),
    ]

    mois = models.CharField(max_length=200, choices=MOIS_CHOICE)
    site = models.ForeignKey(SiteUnique, on_delete=models.CASCADE)
    menages = models.PositiveBigIntegerField(default=0)
    individus = models.PositiveBigIntegerField(default=0)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.mois} - {self.site.nom}"
    
    @property
    def mois_name(self):
        return dict(self.MOIS_CHOICE)[self.mois]
