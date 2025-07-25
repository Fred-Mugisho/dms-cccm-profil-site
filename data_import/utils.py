from typing import Dict, List, Tuple, Optional, Any
from dataclasses import dataclass
import logging

from utils.functions import *
from .models import *


@dataclass
class LocationData:
    """Données de localisation d'un site"""

    province: str = ""
    code_province: str = ""
    territoire: str = ""
    code_territoire: str = ""
    zone_sante: str = ""
    code_zone_sante: str = ""
    type_site: str = ""
    longitude: Optional[float] = None
    latitude: Optional[float] = None


@dataclass
class MouvementData:
    """Données de mouvement"""

    menages: int = 0
    individus: int = 0
    pvh: int = 0
    date_mise_a_jour: str = ""


class DataImportError(Exception):
    """Erreur d'importation"""

    pass


class DataImportService:
    """Service d'importation des données de déplacement"""

    # Mois dans l'ordre chronologique
    SHEETS_CONFIG: List[Tuple[str, str]] = [
        ("Mai2023", "2023-05-31"),
        ("Juin2023", "2023-06-30"),
        ("Juillet2023", "2023-07-31"),
        ("Aout2023", "2023-08-31"),
        ("Sept2023", "2023-09-30"),
        ("Oct2023", "2023-10-31"),
        ("Nov2023", "2023-11-30"),
        ("Dec2023", "2023-12-31"),
        ("Janv2024", "2024-01-31"),
        ("Fev2024", "2024-02-28"),
        ("Mars2024", "2024-03-31"),
        ("Avril2024", "2024-04-30"),
        ("Mai2024", "2024-05-31"),
        ("Juin2024", "2024-06-30"),
        ("Juillet2024", "2024-07-31"),
        ("Aout2024", "2024-08-31"),
        ("Sept2024", "2024-09-30"),
        ("Oct2024", "2024-10-31"),
        ("Nov2024", "2024-11-30"),
        ("Janv2025", "2025-01-31"),
        ("Fev2025", "2025-02-28"),
        ("Mars2025", "2025-03-31"),
    ]

    # Position des colonnes Excel
    COLUMN_INDICES = {
        "province": 1,
        "code_province": 2,
        "territoire": 3,
        "code_territoire": 4,
        "zone_sante": 5,
        "code_zone_sante": 6,
        "nom_site": 7,
        "code_site": 8,
        "type_site": 9,
        "longitude": 10,
        "latitude": 11,
        "menages": 12,
        "individus": 13,
    }

    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def extract_location_data(self, row: Tuple[Any, ...]) -> LocationData:
        """Extrait les données de localisation"""
        try:
            return LocationData(
                province=safe_str(row[self.COLUMN_INDICES["province"]]).strip(),
                code_province=safe_str(
                    row[self.COLUMN_INDICES["code_province"]]
                ).strip(),
                territoire=safe_str(row[self.COLUMN_INDICES["territoire"]]).strip(),
                code_territoire=safe_str(
                    row[self.COLUMN_INDICES["code_territoire"]]
                ).strip(),
                zone_sante=safe_str(row[self.COLUMN_INDICES["zone_sante"]]).strip(),
                code_zone_sante=safe_str(
                    row[self.COLUMN_INDICES["code_zone_sante"]]
                ).strip(),
                type_site=safe_str(row[self.COLUMN_INDICES["type_site"]]).strip(),
                longitude=safe_float(row[self.COLUMN_INDICES["longitude"]]),
                latitude=safe_float(row[self.COLUMN_INDICES["latitude"]]),
            )
        except Exception as e:
            raise DataImportError(f"Erreur extraction localisation: {e}")

    def extract_mouvement_data(
        self, row: Tuple[Any, ...], default_date: str
    ) -> MouvementData:
        """Extrait les données de mouvement"""
        menages = safe_int(row[self.COLUMN_INDICES["menages"]])
        individus = safe_int(row[self.COLUMN_INDICES["individus"]])

        return MouvementData(
            menages=abs(menages),
            individus=abs(individus),
            pvh=0,
            date_mise_a_jour=default_date,
        )

    def validate_row_data(self, row: Tuple[Any, ...]) -> bool:
        """Valide une ligne de données"""
        if not row or len(row) <= self.COLUMN_INDICES["nom_site"]:
            return False

        nom_site = row[self.COLUMN_INDICES["nom_site"]]
        return nom_site and str(nom_site).strip()

    def create_site_data(
        self, location_data: LocationData, row: Tuple[Any, ...]
    ) -> Dict[str, Any]:
        """Crée les données d'un site"""
        return {
            "province": location_data.province,
            "code_province": location_data.code_province,
            "territoire": location_data.territoire,
            "code_territoire": location_data.code_territoire,
            "zone_sante": location_data.zone_sante,
            "code_zone_sante": location_data.code_zone_sante,
            "type_site": location_data.type_site,
            "longitude": location_data.longitude,
            "latitude": location_data.latitude,
            "nom_site": safe_str(row[self.COLUMN_INDICES["nom_site"]]).strip().upper(),
            "code_site": safe_str(row[self.COLUMN_INDICES["code_site"]]).strip(),
            "sous_mecanisme": True,
        }

    def save_site_and_mouvement(
        self, site_data: Dict[str, Any], movement_data: MouvementData
    ) -> None:
        """Sauvegarde site et mouvement"""
        try:
            site_instance, created = SiteDeplace.objects.get_or_create(
                nom_site=site_data["nom_site"],
                defaults=site_data,
            )

            if created:
                self.logger.info(f"Nouveau site: {site_data['nom_site']}")

            TemporalMouvementDeplace.objects.create(
                site=site_instance,
                date_mise_a_jour=movement_data.date_mise_a_jour,
                menages=movement_data.menages,
                individus=movement_data.individus,
                pvh=movement_data.pvh,
            )

        except Exception as e:
            raise DataImportError(f"Erreur sauvegarde {site_data['nom_site']}: {e}")

    def process_sheet_data_v3(self, sheet, sheet_name: str, default_date: str) -> None:
        """Traite une feuille Excel"""
        data_saved = 0

        try:
            # TemporalMouvementDeplace.objects.all().delete()
            self.logger.info(f"Traitement feuille: {sheet_name}")

            for row_num, row in enumerate(
                sheet.iter_rows(min_row=2, values_only=True), start=2
            ):
                try:
                    if not self.validate_row_data(row):
                        continue

                    location_data = self.extract_location_data(row)
                    movement_data = self.extract_mouvement_data(row, default_date)
                    site_data = self.create_site_data(location_data, row)

                    self.save_site_and_mouvement(site_data, movement_data)
                    data_saved += 1

                except Exception as e:
                    self.logger.warning(f"Erreur ligne {row_num}: {e}")
                    continue

            # Générer les variations
            # variation_result = self.generate_variation_data()
            # self.logger.info(f"Variations: {variation_result}")
            self.logger.info(
                f"Feuille {sheet_name} traitée: {data_saved} enregistrements"
            )

        except Exception as e:
            self.logger.error(f"Erreur critique feuille {sheet_name}: {e}")
            raise DataImportError(f"Erreur traitement {sheet_name}: {e}")
        
    def create_variation(self, site, date, menages, individus, type_mouvement):
        """Version corrigée avec validation des données"""
        if menages == 0 and individus == 0:
            return
        
        # Validation des paramètres
        if menages < 0 or individus < 0:
            self.logger.warning(f"Valeurs négatives détectées pour {site.nom_site}: menages={menages}, individus={individus}")
        
        mvt = MouvementDeplace.objects.create(
            site=site,
            date_mise_a_jour=date,
            menages=abs(menages),
            individus=abs(individus),
            type_mouvement=type_mouvement,
        )
        mvt.save_democraphic_data()

    def generate_variation_data(self) -> str:
        """
        Génère les variations mensuelles.
        Logique:
        - Compare mois courant vs mois précédent
        - Site fermé = sortie du total cumulé depuis le début
        """
        try:
            self.logger.info("Génération des variations")

            sites = SiteDeplace.objects.all()

            if not sites.exists():
                return "Aucun site enregistré"

            variation_count = 0
            dates_ordered = [date for _, date in self.SHEETS_CONFIG if date is not None]
            
            # Construction du dictionnaire des sites par mois
            sites_par_mois = {}
            for date in dates_ordered:
                mouvements = TemporalMouvementDeplace.objects.filter(date_mise_a_jour=date)
                sites_par_mois[date] = {m.site.nom_site.upper() for m in mouvements}  # Utilisation d'un set
                
            for site in sites:
                mouvements_site = site.mouvements_temporaire()
                if not mouvements_site:
                    continue
                
                mvt_precedent = None
                for mvt in mouvements_site:
                    if mvt_precedent is not None:
                        # Vérification si le site est fermé (absent du mois courant mais présent le mois précédent)
                        site_present_mois_courant = site.nom_site.upper() in sites_par_mois.get(mvt.date_mise_a_jour, set())
                        site_present_mois_precedent = site.nom_site.upper() in sites_par_mois.get(mvt_precedent.date_mise_a_jour, set())
                        
                        if site_present_mois_precedent and not site_present_mois_courant:
                            # Site fermé : sortie du total cumulé
                            total_menages, total_individus = site.total_cumule_menages_individus()
                            self.create_variation(site, mvt.date_mise_a_jour, total_menages, total_individus, "sortie")
                            variation_count += 1
                        else:
                            # Calcul des deltas
                            delta_menages = mvt.menages - mvt_precedent.menages
                            delta_individus = mvt.individus - mvt_precedent.individus
                            
                            # Détermination du type de mouvement
                            if delta_individus > 0:
                                type_mouvement = 'entree'
                            elif delta_individus < 0:
                                type_mouvement = 'sortie'
                            else:
                                # Delta = 0, on peut ignorer ou traiter selon la logique métier
                                continue
                            
                            self.create_variation(site, mvt.date_mise_a_jour, abs(delta_menages), abs(delta_individus), type_mouvement)
                            variation_count += 1
                    else:
                        # Premier mois : toujours une entrée
                        self.create_variation(site, mvt.date_mise_a_jour, mvt.menages, mvt.individus, "entree")
                        variation_count += 1
                        
                    mvt_precedent = mvt
                    
            return f"{variation_count} variations enregistrées"

        except Exception as e:
            error_msg = f"Erreur génération variations: {e}"
            self.logger.error(error_msg)
            raise DataImportError(error_msg)

    def statistiques(self) -> Dict[str, Any]:
        """Génère les statistiques"""
        try:
            from .serializers import SiteDeplaceSerializer

            sites = SiteDeplace.objects.all()
            if not sites.exists():
                return {
                    "entrees_individus": 0,
                    "sorties_individus": 0,
                    "total_individus": 0,
                    "entrees_menages": 0,
                    "sorties_menages": 0,
                    "total_menages": 0,
                    "nombre_sites": 0,
                    "sites": [],
                }

            entrees_individus_total = 0
            sorties_individus_total = 0
            entrees_menages_total = 0
            sorties_menages_total = 0
            sites_response = []

            for site in sites:
                mouvements = MouvementDeplace.objects.filter(site=site)

                entrees_individus_site = sum(
                    [m.individus for m in mouvements if m.type_mouvement == "entree"]
                )
                sorties_individus_site = sum(
                    [m.individus for m in mouvements if m.type_mouvement == "sortie"]
                )
                entrees_menages_site = sum(
                    [m.menages for m in mouvements if m.type_mouvement == "entree"]
                )
                sorties_menages_site = sum(
                    [m.menages for m in mouvements if m.type_mouvement == "sortie"]
                )

                entrees_individus_total += entrees_individus_site
                sorties_individus_total += sorties_individus_site
                entrees_menages_total += entrees_menages_site
                sorties_menages_total += sorties_menages_site

                site_data = SiteDeplaceSerializer(site).data
                site_data.update(
                    {
                        "individus": entrees_individus_site - sorties_individus_site,
                        "menages": entrees_menages_site - sorties_menages_site,
                        "entrees_individus": entrees_individus_site,
                        "sorties_individus": sorties_individus_site,
                        "entrees_menages": entrees_menages_site,
                        "sorties_menages": sorties_menages_site,
                    }
                )
                sites_response.append(site_data)

            return {
                "entrees_individus": entrees_individus_total,
                "sorties_individus": sorties_individus_total,
                "total_individus": entrees_individus_total - sorties_individus_total,
                "entrees_menages": entrees_menages_total,
                "sorties_menages": sorties_menages_total,
                "total_menages": entrees_menages_total - sorties_menages_total,
                "nombre_sites": len(sites_response),
                "sites": sites_response,
            }

        except Exception as e:
            error_msg = f"Erreur génération statistiques: {e}"
            self.logger.error(error_msg)
            raise DataImportError(error_msg)
