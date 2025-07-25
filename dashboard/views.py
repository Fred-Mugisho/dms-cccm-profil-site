from rest_framework.response import Response
from rest_framework import status
from .models import *
from datetime import date
from .serializers import *
from rest_framework.decorators import api_view
# from dms_cccm import settings
from .services import sync_service
from utils.functions import *

PROVINCES_URGENTS = [
    {"province": "Nord-Kivu", "homme": 0, "femme": 0},
    {"province": "Sud-Kivu", "homme": 0, "femme": 0},
    {"province": "Ituri", "homme": 0, "femme": 0},
    {"province": "Tanganyika", "homme": 0, "femme": 0},
    {"province": "Mai-Ndombe", "homme": 0, "femme": 0},
    {"province": "Kasai", "homme": 0, "femme": 0},
    {"province": "Kasai Central", "homme": 0, "femme": 0},
    {"province": "Haut-Uélé", "homme": 0, "femme": 0},
    {"province": "Bas-Uélé", "homme": 0, "femme": 0},
    {"province": "Maniema", "homme": 0, "femme": 0},
]

TRANCHES_AGE = [
    {"tranche": "0-4", "hommes": 0, "femmes": 0},
    {"tranche": "5-11", "hommes": 0, "femmes": 0},
    {"tranche": "12-17", "hommes": 0, "femmes": 0},
    {"tranche": "18-24", "hommes": 0, "femmes": 0},
    {"tranche": "25-59", "hommes": 0, "femmes": 0},
    {"tranche": "60+", "hommes": 0, "femmes": 0},
]

TYPES_MOUVEMENT_ENTREE = ["naissance", "reunification", "entree"]
TYPES_MOUVEMENT_SORTIE = ["deces", "sortie", "fermeture_site", "dementelement_site"]

TYPES_MOUVEMENT = [
    {"type_mouvement": "naissance", "label": "Naissance", "nombre": 0},
    {"type_mouvement": "reunification", "label": "Reunification", "nombre": 0},
    {"type_mouvement": "entree", "label": "Nouvelles arrivées", "nombre": 0},
    {"type_mouvement": "deces", "label": "Décès", "nombre": 0},
    {"type_mouvement": "sortie", "label": "Départ", "nombre": 0},
    {"type_mouvement": "fermeture_site", "label": "Fermeture site", "nombre": 0},
    {
        "type_mouvement": "dementelement_site",
        "label": "Démentèlement site",
        "nombre": 0,
    },
]

defaultYear = date.today().year
MOIS_ANNEE = [
    {"mois": 1, "annee": defaultYear, "entrees": 0, "sorties": 0},
    {"mois": 2, "annee": defaultYear, "entrees": 0, "sorties": 0},
    {"mois": 3, "annee": defaultYear, "entrees": 0, "sorties": 0},
    {"mois": 4, "annee": defaultYear, "entrees": 0, "sorties": 0},
    {"mois": 5, "annee": defaultYear, "entrees": 0, "sorties": 0},
    {"mois": 6, "annee": defaultYear, "entrees": 0, "sorties": 0},
    {"mois": 7, "annee": defaultYear, "entrees": 0, "sorties": 0},
    {"mois": 8, "annee": defaultYear, "entrees": 0, "sorties": 0},
    {"mois": 9, "annee": defaultYear, "entrees": 0, "sorties": 0},
    {"mois": 10, "annee": defaultYear, "entrees": 0, "sorties": 0},
    {"mois": 11, "annee": defaultYear, "entrees": 0, "sorties": 0},
    {"mois": 12, "annee": defaultYear, "entrees": 0, "sorties": 0},
]

TYPES_SITES = [
    {
        "type_site": "Site Planifié",
        "nombre_individus": 0,
        "nombre_menages": 0,
        "nombre_sites": 0,
    },
    {
        "type_site": "Site Spontané",
        "nombre_individus": 0,
        "nombre_menages": 0,
        "nombre_sites": 0,
    },
    {
        "type_site": "Centre Collectif",
        "nombre_individus": 0,
        "nombre_menages": 0,
        "nombre_sites": 0,
    },
]


@api_view(["GET"])
def dashboard(request):
    try:
        # sync_service.perform_sync()
        # Récupération des mouvements avec gestion d'erreur
        mouvements = MouvementDeplace.objects.all().order_by("date_enregistrement")
        
        # Recuperation des coordonnées des sites
        coordonnees_sites = CoordonneesSite.objects.all().order_by("site_name")
        
        # Filtres - application des filtres sur les mouvements
        province_param = request.GET.get("province")
        territoire_param = request.GET.get("territoire")
        zone_sante_param = request.GET.get("zone_sante")
        site_param = request.GET.get("site")
        coordinateur = request.GET.get("coordinateur")
        gestionnaire_param = request.GET.get("gestionnaire")
        sous_mecanisme_param = request.GET.get("sous_mecanisme")
        deadline_param = request.GET.get("deadline")
        
        deadline = date.today()

        # Application des filtres si présents
        if province_param:
            mouvements = mouvements.filter(province=province_param)
            coordonnees_sites = coordonnees_sites.filter(province=province_param)
        if territoire_param:
            mouvements = mouvements.filter(territoire=territoire_param)
            coordonnees_sites = coordonnees_sites.filter(territoire=territoire_param)
        if zone_sante_param:
            mouvements = mouvements.filter(zone_sante=zone_sante_param)
            coordonnees_sites = coordonnees_sites.filter(zone_sante=zone_sante_param)
        if site_param:
            mouvements = mouvements.filter(site=site_param)
            coordonnees_sites = coordonnees_sites.filter(site_name=site_param)
        if coordinateur:
            mouvements = mouvements.filter(coordinateur_site=coordinateur)
            coordonnees_sites = coordonnees_sites.filter(coordinateur_site=coordinateur)
        if gestionnaire_param:
            mouvements = mouvements.filter(gestionnaire_site=gestionnaire_param)
            coordonnees_sites = coordonnees_sites.filter(gestionnaire_site=gestionnaire_param)
        if sous_mecanisme_param and sous_mecanisme_param in ["0", "1"]:
            sous_mecanisme = True if sous_mecanisme_param == "1" else False
            mouvements = mouvements.filter(sous_mecanisme=sous_mecanisme)
            coordonnees_sites = coordonnees_sites.filter(sous_mecanisme=sous_mecanisme)
        if deadline_param:
            deadline = datetime.strptime(deadline_param, "%Y-%m-%d").date()
            mouvements = mouvements.filter(date_enregistrement__lte=deadline)

        # Initialisation des variables
        hommes = femmes = personnes_vivant_avec_handicaps = menages = entrees = sorties = 0
        enfants = adultes = personnes_agees = 0

        # Copie profonde des structures pour éviter les modifications des constantes
        tendances_deplacement_12_mois = [dict(mois=m["mois"], annee=deadline.year, entrees=0, sorties=0) for m in MOIS_ANNEE]
        repartition_par_tranche_age = [
            dict(tranche=tr["tranche"], hommes=0, femmes=0) for tr in TRANCHES_AGE
        ]
        distribution_par_province_touchees = [
            dict(province=p["province"], homme=0, femme=0) for p in PROVINCES_URGENTS
        ]
        repartition_par_type_entree = [
            dict(type_mouvement=t["type_mouvement"], label=t["label"], nombre=0)
            for t in TYPES_MOUVEMENT
            if t["type_mouvement"] in TYPES_MOUVEMENT_ENTREE
        ]
        repartition_par_type_sortie = [
            dict(type_mouvement=t["type_mouvement"], label=t["label"], nombre=0)
            for t in TYPES_MOUVEMENT
            if t["type_mouvement"] in TYPES_MOUVEMENT_SORTIE
        ]
        par_type_sites = [dict(type_site=t["type_site"], nombre_individus=0, nombre_menages=0, nombre_sites=0) for t in TYPES_SITES]

        coordonnees_sites_serializer = CoordonneesSiteSerializer(coordonnees_sites, many=True).data

        # Traitement des mouvements
        for m in mouvements:
            # Vérification de l'existence des attributs avec valeurs par défaut

            type_mouvement = m.typemouvement

            menages_mvt = m.menage or 0
            pdi_mvt = m.individus or 0
            pvh_mvt = m.personne_vivant_handicape or 0

            if (
                type_mouvement in TYPES_MOUVEMENT_ENTREE
                or type_mouvement == "donnee_brute"
            ):
                entrees += pdi_mvt
                menages += menages_mvt
                personnes_vivant_avec_handicaps += pvh_mvt
            elif type_mouvement in TYPES_MOUVEMENT_SORTIE:
                sorties += pdi_mvt
                menages -= menages_mvt
                personnes_vivant_avec_handicaps -= pvh_mvt

            # Sexe par tranche d'âge avec gestion des attributs manquants
            tranche_map = {
                "0-4": (
                    m.individu_tranche_age_0_4_h or 0,
                    m.individu_tranche_age_0_4_f or 0,
                ),
                "5-11": (
                    m.individu_tranche_age_5_11_f or 0,
                    m.individu_tranche_age_5_11_h or 0,
                ),
                "12-17": (
                    m.individu_tranche_age_12_17_h,
                    m.individu_tranche_age_12_17_f,
                ),
                "18-24": (
                    m.individu_tranche_age_18_24_h,
                    m.individu_tranche_age_18_24_f,
                ),
                "25-59": (
                    m.individu_tranche_age_25_59_h,
                    m.individu_tranche_age_25_59_f,
                ),
                "60+": (
                    m.individu_tranche_age_60_h,
                    m.individu_tranche_age_60_f,
                ),
            }

            # Calcul des totaux par tranche d'âge
            for tranche in repartition_par_tranche_age:
                h, f = tranche_map[tranche["tranche"]]
                if type_mouvement in TYPES_MOUVEMENT_ENTREE:
                    tranche["hommes"] += h
                    tranche["femmes"] += f
                    hommes += h
                    femmes += f
                    if tranche["tranche"] in ["0-4", "5-11", "12-17"]:
                        enfants += h + f
                    elif tranche["tranche"] in ["18-24", "25-59"]:
                        adultes += h + f
                    elif tranche["tranche"] == "60+":
                        personnes_agees += h + f
                elif type_mouvement in TYPES_MOUVEMENT_SORTIE:
                    tranche["hommes"] -= h
                    tranche["femmes"] -= f
                    hommes -= h
                    femmes -= f
                    if tranche["tranche"] in ["0-4", "5-11", "12-17"]:
                        enfants -= h + f
                    elif tranche["tranche"] in ["18-24", "25-59"]:
                        adultes -= h + f
                    elif tranche["tranche"] == "60+":
                        personnes_agees -= h + f

            # Classification par type de mouvement
            if type_mouvement in TYPES_MOUVEMENT_ENTREE:
                for type_mvt in repartition_par_type_entree:
                    if type_mouvement == type_mvt["type_mouvement"]:
                        type_mvt["nombre"] += m.individus
                        break
                    
            elif type_mouvement in TYPES_MOUVEMENT_SORTIE:
                for type_mvt in repartition_par_type_sortie:
                    if type_mouvement == type_mvt["type_mouvement"]:
                        type_mvt["nombre"] += m.individus
                        break

            # Distribution par province urgente
            province_mouvement = m.province
            for p in distribution_par_province_touchees:
                if province_mouvement == p["province"]:
                    if type_mouvement in TYPES_MOUVEMENT_ENTREE:
                        p["homme"] += sum([tranche_map[t][0] for t in tranche_map])
                        p["femme"] += sum([tranche_map[t][1] for t in tranche_map])
                    elif type_mouvement in TYPES_MOUVEMENT_SORTIE:
                        p["homme"] -= sum([tranche_map[t][0] for t in tranche_map])
                        p["femme"] -= sum([tranche_map[t][1] for t in tranche_map])
                    break

            # Tendance mensuelle - vérification de la date
            date_enregistrement = m.date_enregistrement
            if date_enregistrement:
                mois = date_enregistrement.month
                annee = date_enregistrement.year

                for mois_data in tendances_deplacement_12_mois:
                    if mois_data["mois"] == mois and mois_data["annee"] == annee:
                        if type_mouvement in TYPES_MOUVEMENT_ENTREE:
                            mois_data["entrees"] += m.individus
                        elif type_mouvement in TYPES_MOUVEMENT_SORTIE:
                            mois_data["sorties"] += m.individus
                        break

            # Type de site
            type_site_mouvement = m.type_site
            for s in par_type_sites:
                site_type = s["type_site"]
                s["nombre_sites"] = coordonnees_sites.filter(type_site=site_type).count()
                if type_site_mouvement == site_type:
                    if type_mouvement in TYPES_MOUVEMENT_ENTREE:
                        s["nombre_individus"] += m.individus
                        s["nombre_menages"] += m.menage
                    elif type_mouvement in TYPES_MOUVEMENT_SORTIE:
                        s["nombre_individus"] -= m.individus
                        s["nombre_menages"] -= m.menage
                    break
        
        total_pdi = max(0, entrees - sorties)
        pourcentage_hommes = round((hommes / total_pdi) * 100, 2) if total_pdi != 0 else 0
        pourcentage_femmes = round((femmes / total_pdi) * 100, 2) if total_pdi != 0 else 0
        # Construction de la réponse
        response = {
            "params": {
                "province": province_param,
                "territoire": territoire_param,
                "zone_sante": zone_sante_param,
                "site": site_param,
                "coordinateur": coordinateur,
                "gestionnaire": gestionnaire_param,
                "sous_mecanisme": sous_mecanisme_param,
                "deadline": deadline_param,
            },
            "profil_demographique": {
                "general": {
                    "total_pdi": total_pdi,
                    "hommes": max(0, hommes),
                    "femmes": max(0, femmes),
                    "pourcentage_hommes": pourcentage_hommes,
                    "pourcentage_femmes": pourcentage_femmes,
                    "personnes_vivant_avec_handicaps": max(0, personnes_vivant_avec_handicaps),
                    "menages": max(0, menages),
                    "entrees": entrees,
                    "sorties": sorties,
                    "adultes": max(0, adultes),
                    "enfants": max(0, enfants),
                    "personnes_agees": max(0, personnes_agees),
                },
                "par_type_sites": par_type_sites,
                "repartition_par_tranche_age": repartition_par_tranche_age,
                "distribution_par_province_touchees": distribution_par_province_touchees,
                "repartition_par_type_entree": repartition_par_type_entree,
                "repartition_par_type_sortie": repartition_par_type_sortie,
                "par_type_mouvement": repartition_par_type_entree + repartition_par_type_sortie,
            },
            "tendances_deplacement_12_mois": tendances_deplacement_12_mois,
            "coordonnees_sites": coordonnees_sites_serializer,
        }
        return Response(response, status=status.HTTP_200_OK)
    except Exception as e:
        return Response(
            {"message": f"Erreur serveur: {str(e)}"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

@api_view(["GET"])
def refresh_dashboard(request):
    try:
        sync_service.perform_sync()
        return Response(
            {"message": "Données du tableau de bord rafraîchies avec succès."},
            status=status.HTTP_200_OK,
        )
    except Exception as e:
        return Response(
            {"message": f"Erreur serveur: {str(e)}"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )