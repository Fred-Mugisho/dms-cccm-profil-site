from typing import Dict, List, Tuple, Optional, Any
from dataclasses import dataclass
import logging

from utils.functions import *
from .models import *


@dataclass
class SiteData:
    """Données d'un site"""

    province: str = ""
    code_province: str = ""
    territoire: str = ""
    code_territoire: str = ""
    zone_sante: str = ""
    code_zone_sante: str = ""
    nom_site: str = ""
    type_site: str = ""
    sous_mecanisme: bool = False
    longitude: Optional[float] = None
    latitude: Optional[float] = None
    gestionnaire: Optional[str] = None
    coordinateur: Optional[str] = None
    menages_initiaux: int = 0
    individus_initiaux: int = 0


@dataclass
class MouvementMensuelData:
    """Données de mouvement mensuel"""

    nom_site: str = ""
    augm_dimin_menages: int = 0
    augm_dimin_individus: int = 0
    menages: int = 0
    individus: int = 0
    pvh: int = 0
    date_mise_a_jour: str = ""


class DataImportError(Exception):
    """Erreur d'importation"""
    pass


class DataImportService:
    """Service d'importation des données de déplacement"""

    SHEETS_CONFIG: List[Tuple[str, str]] = [
        ("Sites", "2023-05-31"),
        ("Mai2023", "2023-05-31"),
        ("Juin2023", "2023-06-30"),
        ("Juillet2023", "2023-07-31"),
        ("Aout2023", "2023-08-31"),
        ("Sept2023", "2023-09-30"),
        ("Oct2023", "2023-10-31"),
        ("Nov2023", "2023-11-30"),
        ("Dec2023", "2023-12-31"),
    ]

    COLUMN_INDICES_SITES = {
        "province": 1,
        "code_province": 2,
        "territoire": 3,
        "code_territoire": 4,
        "zone_sante": 5,
        "code_zone_sante": 6,
        "nom_site": 7,
        "type_site": 8,
        "mecanisme": 9,
        "longitude": 10,
        "latitude": 11,
        "menages_initiaux": 12,
        "individus_initiaux": 13,
        "gestionnaire": 14,
        "coordinateur": 15,
    }

    COLUMN_INDICES_MOUVEMENT = {
        "nom_site": 1,
        "up_down_menage": 2,
        "up_down_individu": 3,
        "menages": 4,
        "individus": 5,
        "date_mise_a_jour": 6,
    }

    def match_date_par_mois(self, mois: str):
        for date in self.SHEETS_CONFIG:
            if date[0] == mois:
                return date[1]
        return None

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.mouvements_liste = []

    def extract_site_data(self, row: Tuple[Any, ...]) -> Optional[SiteData]:
        try:
            mecanisme = safe_int(row[self.COLUMN_INDICES_SITES["mecanisme"]])
            sous_mecanisme = True if mecanisme == 1 else False
            site = SiteData(
                province=safe_str(row[self.COLUMN_INDICES_SITES["province"]]).strip(),
                code_province=safe_str(row[self.COLUMN_INDICES_SITES["code_province"]]).strip(),
                territoire=safe_str(row[self.COLUMN_INDICES_SITES["territoire"]]).strip(),
                code_territoire=safe_str(row[self.COLUMN_INDICES_SITES["code_territoire"]]).strip(),
                zone_sante=safe_str(row[self.COLUMN_INDICES_SITES["zone_sante"]]).strip(),
                code_zone_sante=safe_str(row[self.COLUMN_INDICES_SITES["code_zone_sante"]]).strip(),
                nom_site=safe_str(row[self.COLUMN_INDICES_SITES["nom_site"]]).strip(),
                type_site=safe_str(row[self.COLUMN_INDICES_SITES["type_site"]]).strip(),
                sous_mecanisme=sous_mecanisme,
                longitude=safe_float(row[self.COLUMN_INDICES_SITES["longitude"]]),
                latitude=safe_float(row[self.COLUMN_INDICES_SITES["latitude"]]),
                gestionnaire=safe_str(row[self.COLUMN_INDICES_SITES["gestionnaire"]]).strip(),
                coordinateur=safe_str(row[self.COLUMN_INDICES_SITES["coordinateur"]]).strip(),
                menages_initiaux=safe_int(row[self.COLUMN_INDICES_SITES["menages_initiaux"]]),
                individus_initiaux=safe_int(row[self.COLUMN_INDICES_SITES["individus_initiaux"]]),
            )
            return site
        except Exception as e:
            self.logger.error(f"Erreur extraction site: {e}")
            return None

    def extract_mouvement_mensuel_data(
        self, row: Tuple[Any, ...], default_date: str
    ) -> MouvementMensuelData:
        """Extrait les données de mouvement mensuel"""
        nom_site = safe_str(row[self.COLUMN_INDICES_MOUVEMENT["nom_site"]]).strip()
        augm_dimin_menages = safe_int(row[self.COLUMN_INDICES_MOUVEMENT["up_down_menage"]])
        augm_dimin_individus = safe_int(row[self.COLUMN_INDICES_MOUVEMENT["up_down_individu"]])
        menages = safe_int(row[self.COLUMN_INDICES_MOUVEMENT["menages"]])
        individus = safe_int(row[self.COLUMN_INDICES_MOUVEMENT["individus"]])

        return MouvementMensuelData(
            nom_site=nom_site.lower(),
            augm_dimin_menages=augm_dimin_menages,
            augm_dimin_individus=augm_dimin_individus,
            menages=abs(menages),
            individus=abs(individus),
            pvh=0,
            date_mise_a_jour=default_date,
        )

    def validate_row_data(self, row: Tuple[Any, ...]) -> bool:
        """Valide une ligne de données"""
        if not row or len(row) <= self.COLUMN_INDICES_MOUVEMENT["nom_site"]:
            return False

        nom_site = row[self.COLUMN_INDICES_MOUVEMENT["nom_site"]]
        return bool(nom_site and str(nom_site).strip())

    def payload_create_site(self, site_data: SiteData) -> Dict[str, Any]:
        return {
            "province": site_data.province.lower(),
            "code_province": site_data.code_province,
            "territoire": site_data.territoire.lower(),
            "code_territoire": site_data.code_territoire,
            "zone_sante": site_data.zone_sante.lower(),
            "code_zone_sante": site_data.code_zone_sante,
            "type_site": site_data.type_site,
            "longitude": site_data.longitude,
            "latitude": site_data.latitude,
            "nom_site": site_data.nom_site.lower(),
            "sous_mecanisme": site_data.sous_mecanisme,
            "gestionnaire": site_data.gestionnaire,
            "coordinateur": site_data.coordinateur,
        }

    def save_site(self, payload: Dict[str, Any], site_data: SiteData) -> None:
        """Sauvegarde site"""
        try:
            if site_data.nom_site == "":
                return
            
            site_instance, created = SiteDeplace.objects.update_or_create(
                nom_site=site_data.nom_site.lower(),
                defaults=payload,
            )
            if created:
                self.logger.info(f"Nouveau site: {site_data.nom_site}")
            else:
                self.logger.info(f"Mise à jour site: {site_data.nom_site}")
        except Exception as e:
            self.logger.error(f"Erreur sauvegarde {site_data.nom_site}: {e}")

    def save_mouvement(self, mouvement_data: MouvementMensuelData) -> None:
        """Sauvegarde mouvement"""
        try:
            site_deplace = SiteDeplace.objects.filter(nom_site=mouvement_data.nom_site).first()
            if not site_deplace:
                self.logger.error(f"Site {mouvement_data.nom_site} introuvable")
                return
            
            total_menages, total_individus = site_deplace.total_cumule_menages_individus()
            is_first_movement_site = total_menages == 0 and total_individus == 0

            if is_first_movement_site:
                if mouvement_data.menages > 0 or mouvement_data.individus > 0:
                    MouvementDeplace.objects.create(
                        site=site_deplace,
                        type_mouvement="entree",
                        menages=abs(mouvement_data.menages),
                        individus=abs(mouvement_data.individus),
                        pvh=mouvement_data.pvh,
                        date_mise_a_jour=mouvement_data.date_mise_a_jour,
                    ).save_democraphic_data()
            else:
                total_menages, total_individus = site_deplace.total_cumule_menages_individus()
                if mouvement_data.menages == 0 and mouvement_data.individus == 0:
                    if total_menages > 0 or total_individus > 0:
                        MouvementDeplace.objects.create(
                            site=site_deplace,
                            type_mouvement="sortie",
                            menages=abs(total_menages),
                            individus=abs(total_individus),
                            pvh=mouvement_data.pvh,
                            date_mise_a_jour=mouvement_data.date_mise_a_jour,
                        ).save_democraphic_data()
                    return
                
                variation_menages = mouvement_data.menages - total_menages
                variation_individus = mouvement_data.individus - total_individus
                
                if variation_menages > 0 or variation_individus > 0:
                    type_mouvement = "entree"
                elif variation_menages < 0 or variation_individus < 0:
                    type_mouvement = "sortie"
                else:
                    return  # pas de changement
                
                MouvementDeplace.objects.create(
                    site=site_deplace,
                    type_mouvement=type_mouvement,
                    menages=abs(variation_menages),
                    individus=abs(variation_individus),
                    pvh=mouvement_data.pvh,
                    date_mise_a_jour=mouvement_data.date_mise_a_jour,
                ).save_democraphic_data()
        except Exception as e:
            self.logger.error(f"Erreur sauvegarde mouvement {mouvement_data}: {e}")

    def process_sheet_data_v3(self, sheet, sheet_name: str, default_date: str) -> None:
        """Traite une feuille Excel"""
        data_saved = 0
        menages = 0
        individus = 0
        try:
            # self.logger.info(f"Traitement feuille: {sheet_name}")

            for row_num, row in enumerate(sheet.iter_rows(min_row=2, values_only=True), start=2):
                try:
                    if sheet_name == "Sites":
                        site_data = self.extract_site_data(row)
                        if site_data:
                            payload = self.payload_create_site(site_data)
                            self.save_site(payload, site_data)
                    else:
                        if not self.validate_row_data(row):
                            continue
                        mouvement_data = self.extract_mouvement_mensuel_data(row, default_date)
                        self.save_mouvement(mouvement_data)
                        
                        menages += mouvement_data.menages
                        individus += mouvement_data.individus
                    data_saved += 1
                except Exception as e:
                    self.logger.warning(f"Erreur ligne {row_num}: {e}")
                    continue
            
            self.logger.info(f"Traitement feuille: {sheet_name} menages={menages}, individus={individus}")
            self.logger.info(f"------------------------------------------------------------------------------")
            # self.logger.info(f"Feuille {sheet_name} traitée: {data_saved} enregistrements")

        except Exception as e:
            self.logger.error(f"Erreur critique feuille {sheet_name}: {e}")
            raise DataImportError(f"Erreur traitement {sheet_name}: {e}")

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

                entrees_individus_site = sum(m.individus for m in mouvements if m.type_mouvement == "entree")
                sorties_individus_site = sum(m.individus for m in mouvements if m.type_mouvement == "sortie")
                entrees_menages_site = sum(m.menages for m in mouvements if m.type_mouvement == "entree")
                sorties_menages_site = sum(m.menages for m in mouvements if m.type_mouvement == "sortie")

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
