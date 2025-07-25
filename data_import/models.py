from django.db import models

# NOUVELLE REFLEXION
class SiteDeplace(models.Model):
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
    sous_mecanisme = models.BooleanField(default=True)
    
    def __str__(self):
        return self.nom_site
    
    def deltas_menages_individus_type_mouvement(self, menages: int, individus: int):
        mouvements_site = MouvementDeplace.objects.filter(site=self)
        if not mouvements_site.exists():
            return menages, individus, 'entree'
        
        actual_menages = 0
        actual_individus = 0
        for mouvement in mouvements_site:
            actual_menages += mouvement.menages
            actual_individus += mouvement.individus
        
        delta_menages = menages - actual_menages
        delta_individus = individus - actual_individus
        type_mouvement = 'entree' if delta_individus >= 0 else 'sortie'
        
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
            return TemporalMouvementDeplace.objects.filter(site=self).order_by('date_mise_a_jour')
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
    
    def save_democraphic_data(self):
        data = self.extract_demographic_data()
        for cle, valeur in data.items():
            setattr(self, cle, valeur)
        self.save()