import threading
import time
import json
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from requests.exceptions import ChunkedEncodingError
from http.client import IncompleteRead
from datetime import datetime, timedelta
from django.db.models import Sum

from .models import HistoriqueSynchro, CoordonneesSite, MouvementDeplace
import logging

logger = logging.getLogger(__name__)

def normalize_str(s):
    return s.strip().lower() if s else ""

class DataSyncService:
    def __init__(self):
        self.BASE_URL = "http://cccm.expertiserdc.com/api"
        self.sync_interval = 30  # minutes
        self.running = False
        self.thread = None
        self.session = self._create_session()

    def _create_session(self):
        session = requests.Session()
        retry = Retry(total=5, backoff_factor=1, status_forcelist=[502, 503, 504, 522], raise_on_status=False)
        adapter = HTTPAdapter(max_retries=retry)
        session.mount("http://", adapter)
        session.mount("https://", adapter)
        return session

    def should_sync(self):
        last_sync = HistoriqueSynchro.objects.last()
        if not last_sync:
            return True
        return (datetime.now() - last_sync.dernier_synchro.replace(tzinfo=None)) > timedelta(minutes=self.sync_interval)

    def _parse_date(self, date_str):
        try:
            return datetime.strptime(date_str, "%Y-%m-%d").date() if date_str else datetime.now().date()
        except ValueError:
            return datetime.now().date()

    def sync_movements_data_bulk(self, data_movements):
        tranche_map = {
            '0-4': ('individu_tranche_age_0_4_h', 'individu_tranche_age_0_4_f'),
            '5-11': ('individu_tranche_age_5_11_h', 'individu_tranche_age_5_11_f'),
            '12-17': ('individu_tranche_age_12_17_h', 'individu_tranche_age_12_17_f'),
            '18-24': ('individu_tranche_age_18_24_h', 'individu_tranche_age_18_24_f'),
            '25-59': ('individu_tranche_age_25_59_h', 'individu_tranche_age_25_59_f'),
            '60+': ('individu_tranche_age_60_h', 'individu_tranche_age_60_f'),
        }

        mouvements_to_create = []

        for movement in data_movements:
            try:
                activite = movement.get("activite", {})
                if activite.get("statut") != "valide":
                    continue

                tranche_counts = {field: 0 for fields in tranche_map.values() for field in fields}

                for tranche in movement.get("individu_tranche_age", []):
                    sexe = tranche.get("sexe")
                    tranche_age = tranche.get("tranche_age")
                    individus = int(tranche.get("individus", 0))
                    if tranche_age in tranche_map:
                        h_field, f_field = tranche_map[tranche_age]
                        if sexe == "homme":
                            tranche_counts[h_field] += individus
                        elif sexe == "femme":
                            tranche_counts[f_field] += individus

                site = movement.get("site", {})
                zs = movement.get("zone_sante", {})
                territoire = zs.get("territoire", {}) if zs else {}
                province = territoire.get("province", {}) if territoire else {}
                org = movement.get("organisation", {})
                enqueteur = movement.get("enqueteur", {})

                coordinateur = enqueteur.get("coordinateur", {})
                gestionnaire = enqueteur.get("gestionnaire", {})

                date_enr = self._parse_date(movement.get("date_enregistrement"))

                type_mouvement = movement.get("typemouvement", "")
                if type_mouvement == 'donnee_brute':
                    type_mouvement = 'entree'
                elif type_mouvement == 'depart':
                    type_mouvement = 'sortie'

                mouvements_to_create.append(
                    MouvementDeplace(
                        provenance=movement.get("provenance", ""),
                        menage=movement.get("menage", 0),
                        individus=movement.get("individus", 0),
                        personne_vivant_handicape=movement.get("personne_vivant_handicape", 0),
                        typemouvement=type_mouvement,
                        raison=movement.get("raison", ""),
                        statutmouvement=activite.get("statut", ""),
                        province=normalize_str(province.get("nom", "")),
                        territoire=normalize_str(territoire.get("nom", "")),
                        zone_sante=normalize_str(zs.get("nom", "")),
                        site=normalize_str(site.get("nom", "")),
                        type_site=site.get("type_site", ""),
                        coordinateur_site=normalize_str(coordinateur.get("nom")),
                        gestionnaire_site=normalize_str(gestionnaire.get("nom")),
                        sous_mecanisme=bool(site.get("sous_meccanisme_cccm", 0)),
                        organisation=normalize_str(org.get("nom", "")),
                        activite=activite.get("id", 1),
                        enqueteur=normalize_str(enqueteur.get("nom", "")),
                        date_enregistrement=date_enr,
                        **tranche_counts
                    )
                )
            except Exception as e:
                logger.error(f"Erreur préparation mouvement: {e}")

        MouvementDeplace.objects.bulk_create(mouvements_to_create, batch_size=500)
        logger.info(f"{len(mouvements_to_create)} mouvements synchronisés en bulk")
        return len(mouvements_to_create)

    def sync_sites_data_bulk(self, data_sites):
        sites_to_update = []
        for site in data_sites:
            try:
                position = site.get("position", {})
                zs = site.get("zone_sante", {})
                territoire = zs.get("territoire", {}) if zs else {}
                province = territoire.get("province", {}) if territoire else {}
                coordinateur = site.get("coordinateur", {})
                gestionnaire = site.get("gestionnaire", {})
                sous_mecanisme = bool(site.get("sous_meccanisme_cccm", 0))

                obj, created = CoordonneesSite.objects.update_or_create(
                    site_name=normalize_str(site.get("nom", "")),
                    defaults={
                        "type_site": site.get("type_site", ""),
                        "url_map": site.get("url_map", ""),
                        "province": normalize_str(province.get("nom")),
                        "territoire": normalize_str(territoire.get("nom")),
                        "zone_sante": normalize_str(zs.get("nom")),
                        "sous_mecanisme": sous_mecanisme,
                        "coordinateur_site": normalize_str(coordinateur.get("nom")),
                        "gestionnaire_site": normalize_str(gestionnaire.get("nom")),
                        "latitude": float(position.get("latitude", 0)),
                        "longitude": float(position.get("longitude", 0)),
                    }
                )
                sites_to_update.append(obj)
            except Exception as e:
                logger.error(f"Erreur création site: {e}")

        logger.info(f"{len(sites_to_update)} sites synchronisés")
        return len(sites_to_update)

    def calculer_stats_site_bulk(self):
        updates = []
        for coordonnee in CoordonneesSite.objects.all():
            agg = MouvementDeplace.objects.filter(site=coordonnee.site_name).aggregate(
                total_menages=Sum('menage'),
                total_individus=Sum('individus')
            )
            coordonnee.nombre_menages = agg['total_menages'] or 0
            coordonnee.nombre_individus = agg['total_individus'] or 0
            updates.append(coordonnee)
        CoordonneesSite.objects.bulk_update(updates, ['nombre_menages', 'nombre_individus'])
        logger.info("Stats des sites mises à jour en bulk")

    def perform_sync(self):
        logger.info("Début de la synchronisation")
        try:
            mouvements_url = f"{self.BASE_URL}/masterlist/mouvement"
            sites_url = f"{self.BASE_URL}/site/"
            params = {"statut_activite": "valide"}

            resp_mvt = self.session.get(mouvements_url, params=params, timeout=60)
            resp_sites = self.session.get(sites_url, params=params, timeout=60)

            if resp_mvt.status_code == 200 and resp_sites.status_code == 200:
                try:
                    data_movements = resp_mvt.json()
                    data_sites = resp_sites.json()
                except (ChunkedEncodingError, IncompleteRead, json.JSONDecodeError) as e:
                    logger.error(f"Erreur lecture JSON: {e}")
                    return False

                self.sync_movements_data_bulk(data_movements)
                self.sync_sites_data_bulk(data_sites)
                self.calculer_stats_site_bulk()
                HistoriqueSynchro.objects.create()
                logger.info("Synchronisation terminée avec succès")
                return True
            else:
                logger.error(f"Erreur API: mvt={resp_mvt.status_code}, site={resp_sites.status_code}")
                return False

        except requests.RequestException as e:
            logger.error(f"Erreur connexion API: {e}")
            return False
        except Exception as e:
            logger.error(f"Erreur inconnue synchronisation: {e}")
            return False

    def sync_loop(self):
        logger.info("Service de synchro en boucle lancé")
        while self.running:
            start_time = time.time()
            try:
                if self.should_sync():
                    logger.info("Synchro requise")
                    self.perform_sync()
            except Exception as e:
                logger.error(f"Erreur dans la boucle: {e}")
            elapsed = time.time() - start_time
            time.sleep(max(0, 60*self.sync_interval - elapsed))

    def start(self):
        if not self.running:
            self.running = True
            self.thread = threading.Thread(target=self.sync_loop, daemon=True)
            self.thread.start()
            logger.info("Thread synchro démarré")

    def stop(self):
        self.running = False
        if self.thread and self.thread.is_alive():
            self.thread.join(timeout=5)
        logger.info("Service de synchro arrêté")

    def force_sync(self):
        logger.info("Synchro forcée demandée")
        return self.perform_sync()

# Singleton global
sync_service = DataSyncService()
