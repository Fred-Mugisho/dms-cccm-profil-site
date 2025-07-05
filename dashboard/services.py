import threading
import time
import json
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from requests.exceptions import ChunkedEncodingError
from http.client import IncompleteRead

from datetime import datetime, timedelta
from .models import HistoriqueSynchro, CoordonneesSite, MouvementDeplace

import logging
logger = logging.getLogger(__name__)

class DataSyncService:
    def __init__(self):
        self.BASE_URL = "http://cccm.expertiserdc.com/api"
        self.sync_interval = 30  # minutes
        self.running = False
        self.thread = None
        self.session = self.get_session()

    def get_session(self):
        session = requests.Session()
        retry = Retry(
            total=5,
            backoff_factor=1,
            status_forcelist=[502, 503, 504, 522],
            raise_on_status=False
        )
        adapter = HTTPAdapter(max_retries=retry)
        session.mount("http://", adapter)
        session.mount("https://", adapter)
        return session

    def clean_data_store(self):
        try:
            CoordonneesSite.objects.all().delete()
            MouvementDeplace.objects.all().delete()
            logger.info("Données nettoyées avec succès")
        except Exception as e:
            logger.error(f"Erreur lors du nettoyage des données: {e}")

    def calculer_stats_site(self):
        try:
            for coordonnee in CoordonneesSite.objects.all():
                mouvements = MouvementDeplace.objects.filter(site=coordonnee.site_name)
                coordonnee.nombre_menages = sum(m.menage for m in mouvements)
                coordonnee.nombre_individus = sum(m.individus for m in mouvements)
                coordonnee.save()
            logger.info("Statistiques des sites mises à jour")
        except Exception as e:
            logger.error(f"Erreur lors du calcul des statistiques: {e}")

    def should_sync(self):
        try:
            last_sync = HistoriqueSynchro.objects.last()
            if not last_sync:
                return True
            return (datetime.now() - last_sync.dernier_synchro.replace(tzinfo=None)) > timedelta(minutes=self.sync_interval)
        except Exception as e:
            logger.error(f"Erreur lors de la vérification de synchro: {e}")
            return True

    def sync_movements_data(self, data_movements):
        count = 0
        for movement in data_movements:
            try:
                activite = movement.get("activite", {})
                if activite.get("statut", "") != "valide":
                    continue
                
                individu_tranche_age_0_4_f = 0
                individu_tranche_age_5_11_f = 0
                individu_tranche_age_12_17_f = 0
                individu_tranche_age_18_24_f = 0
                individu_tranche_age_25_59_f = 0
                individu_tranche_age_60_f = 0
                individu_tranche_age_0_4_h = 0
                individu_tranche_age_5_11_h = 0
                individu_tranche_age_12_17_h = 0
                individu_tranche_age_18_24_h = 0
                individu_tranche_age_25_59_h = 0
                individu_tranche_age_60_h = 0
                for tranche in movement.get("individu_tranche_age", []):
                    sexe = tranche.get("sexe")
                    tranche_age = tranche.get("tranche_age")
                    individus = int(tranche.get("individus", 0))
                    if sexe == 'femme':
                        if tranche_age == '0-4':
                            individu_tranche_age_0_4_f += individus
                        elif tranche_age == '5-11':
                            individu_tranche_age_5_11_f += individus
                        elif tranche_age == '12-17':
                            individu_tranche_age_12_17_f += individus
                        elif tranche_age == '18-24':
                            individu_tranche_age_18_24_f += individus
                        elif tranche_age == '25-59':
                            individu_tranche_age_25_59_f += individus
                        elif tranche_age == '60+':
                            individu_tranche_age_60_f += individus
                    elif sexe == 'homme':
                        if tranche_age == '0-4':
                            individu_tranche_age_0_4_h += individus
                        elif tranche_age == '5-11':
                            individu_tranche_age_5_11_h += individus
                        elif tranche_age == '12-17':
                            individu_tranche_age_12_17_h += individus
                        elif tranche_age == '18-24':
                            individu_tranche_age_18_24_h += individus
                        elif tranche_age == '25-59':
                            individu_tranche_age_25_59_h += individus
                        elif tranche_age == '60+':
                            individu_tranche_age_60_h += individus

                site = movement.get("site", {})
                zs = movement.get("zone_sante", {})
                territoire = zs.get("territoire", {}) if zs else {}
                province = territoire.get("province", {}) if territoire else {}
                org = movement.get("organisation", {})
                enqueteur = movement.get("enqueteur", {})
                
                coordinateur = enqueteur.get("coordinateur", {})
                gestionnaire = enqueteur.get("gestionnaire", {})

                date_enr = movement.get("date_enregistrement")
                try:
                    date_enr = datetime.strptime(date_enr, "%Y-%m-%d").date() if date_enr else datetime.now().date()
                except ValueError:
                    date_enr = datetime.now().date()
                    
                type_mouvement = movement.get("typemouvement", "")
                if type_mouvement == 'donnee_brute':
                    type_mouvement = 'entree'
                elif type_mouvement == 'depart':
                    type_mouvement = 'sortie'

                MouvementDeplace.objects.create(
                    provenance=movement.get("provenance", ""),
                    menage=movement.get("menage", 0),
                    individus=movement.get("individus", 0),
                    personne_vivant_handicape=movement.get("personne_vivant_handicape", 0),
                    typemouvement=type_mouvement,
                    raison=movement.get("raison", ""),
                    statutmouvement=activite.get("statut", ""),
                    province=province.get("nom", ""),
                    territoire=territoire.get("nom", ""),
                    zone_sante=zs.get("nom", ""),
                    site=site.get("nom", ""),
                    type_site=site.get("type_site", ""),
                    coordinateur_site=coordinateur.get("nom", ""),
                    gestionnaire_site=gestionnaire.get("nom", ""),
                    sous_mecanisme=bool(site.get("sous_meccanisme_cccm", 0)),
                    organisation=org.get("nom", ""),
                    activite=activite.get("id", 1),
                    enqueteur=enqueteur.get("nom", ""),
                    date_enregistrement=date_enr,
                    individu_tranche_age_0_4_f=individu_tranche_age_0_4_f,
                    individu_tranche_age_5_11_f=individu_tranche_age_5_11_f,
                    individu_tranche_age_12_17_f=individu_tranche_age_12_17_f,
                    individu_tranche_age_18_24_f=individu_tranche_age_18_24_f,
                    individu_tranche_age_25_59_f=individu_tranche_age_25_59_f,
                    individu_tranche_age_60_f=individu_tranche_age_60_f,
                    individu_tranche_age_0_4_h=individu_tranche_age_0_4_h,
                    individu_tranche_age_5_11_h=individu_tranche_age_5_11_h,
                    individu_tranche_age_12_17_h=individu_tranche_age_12_17_h,
                    individu_tranche_age_18_24_h=individu_tranche_age_18_24_h,
                    individu_tranche_age_25_59_h=individu_tranche_age_25_59_h,
                    individu_tranche_age_60_h=individu_tranche_age_60_h
                )
                count += 1
            except Exception as e:
                logger.error(f"Erreur création mouvement: {e}")
        logger.info(f"{count} mouvements créés")
        return count

    def sync_sites_data(self, data_sites):
        count = 0
        for site in data_sites:
            try:
                position_data = site.get("position", {})
                zone_sante_data = site.get("zone_sante", {})
                territoire_data = zone_sante_data.get("territoire", {})
                province_data = territoire_data.get("province", {})
                coordinateur_data = site.get("coordinateur", {})
                gestionnaire_data = site.get("gestionnaire", {})
                sous_mecanisme = bool(site.get("sous_meccanisme_cccm", 0))
                
                CoordonneesSite.objects.update_or_create(
                    site_name=site.get("nom", ""),
                    defaults={
                        "type_site": site.get("type_site", ""),
                        "url_map": site.get("url_map", ""),
                        "province": province_data.get("nom", "") if province_data else "",
                        "territoire": territoire_data.get("nom", "") if territoire_data else "",
                        "zone_sante": zone_sante_data.get("nom", "") if zone_sante_data else "",
                        "sous_mecanisme": sous_mecanisme,
                        "coordinateur_site": coordinateur_data.get("nom", "") if coordinateur_data else "",
                        "gestionnaire_site": gestionnaire_data.get("nom", "") if gestionnaire_data else "",
                        "latitude": float(position_data.get("latitude", 0)),
                        "longitude": float(position_data.get("longitude", 0)),
                    }
                )
                count += 1
            except Exception as e:
                logger.error(f"Erreur création site: {e}")
        logger.info(f"{count} sites créés")
        return count

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
                    data_movements = json.loads(resp_mvt.content)
                    data_sites = json.loads(resp_sites.content)
                except (ChunkedEncodingError, IncompleteRead, json.JSONDecodeError) as e:
                    logger.error(f"Erreur lecture JSON: {e}")
                    return False

                self.clean_data_store()
                self.sync_movements_data(data_movements)
                self.sync_sites_data(data_sites)
                self.calculer_stats_site()
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
            try:
                if self.should_sync():
                    logger.info("Synchro requise")
                    if not self.perform_sync():
                        time.sleep(30)
                        continue
                time.sleep(60 * self.sync_interval)
            except Exception as e:
                logger.error(f"Erreur dans la boucle: {e}")
                time.sleep(60)

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
