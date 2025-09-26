from rest_framework.response import Response
from rest_framework import status
from .models import *
from datetime import date, timedelta
from .serializers import *
from rest_framework.decorators import api_view
from .services import sync_service
from utils.functions import *
from dateutil.relativedelta import relativedelta
from django.core.cache import cache
from django.db.models import Sum, Count, Q, F
from django.db.models.functions import ExtractMonth, ExtractYear
from data_import.models import SiteDeplace

PROVINCES_URGENTS = [
    {"province": "nord-kivu", "homme": 0, "femme": 0},
    {"province": "sud-kivu", "homme": 0, "femme": 0},
    {"province": "ituri", "homme": 0, "femme": 0},
    {"province": "tanganyika", "homme": 0, "femme": 0},
    {"province": "mai-ndombe", "homme": 0, "femme": 0},
    {"province": "kasai", "homme": 0, "femme": 0},
    {"province": "kasai Central", "homme": 0, "femme": 0},
    {"province": "haut-uélé", "homme": 0, "femme": 0},
    {"province": "bas-uélé", "homme": 0, "femme": 0},
    {"province": "maniema", "homme": 0, "femme": 0},
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

CACHE_TIMEOUT = 60 * 60 * 24  # 24 heures
CACHE_KEY_COORDINATEURS_GESTIONNAIRES = "coordinateurs_gestionnaires"
CACHE_KEY_DASHBOARD = "dashboard"


@api_view(["GET"])
def coordinateurs_gestionnaires(request):
    try:
        # Vérifie si les données sont déjà en cache
        data = cache.get("coordinateurs_gestionnaires")

        if not data:
            # Exécuter la requête uniquement si pas en cache
            coordinateurs = (
                SiteDeplace.objects
                .filter(~Q(coordinateur__isnull=True), ~Q(coordinateur__exact=""))
                .values_list("coordinateur", flat=True)
                .distinct()
            )

            gestionnaires = (
                SiteDeplace.objects
                .filter(~Q(gestionnaire__isnull=True), ~Q(gestionnaire__exact=""))
                .values_list("gestionnaire", flat=True)
                .distinct()
            )

            data = {
                "coordinateurs": list(coordinateurs),
                "gestionnaires": list(gestionnaires),
            }

            # Stocker le résultat en cache
            cache.set("coordinateurs_gestionnaires", data, CACHE_TIMEOUT)

        return Response(data, status=status.HTTP_200_OK)

    except Exception as e:
        return Response(
            {"message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

def build_cache_key(prefix: str, params: dict) -> str:
    # clé simple, stable et réversible pour chaque combinaison de filtres
    parts = [prefix] + [
        f"{k}={v}" for k, v in sorted(params.items()) if v is not None and v != ""
    ]
    return "|".join(parts)

@api_view(["GET"])
def dashboard_v1(request):
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
        # deadline_param = request.GET.get("deadline")
        date_debut_param = request.GET.get("date_debut")
        date_fin_param = request.GET.get("date_fin")

        # deadline = date.today()
        date_debut = None
        date_fin = date.today()
        
        cache_params = {
            "province": province_param,
            "territoire": territoire_param,
            "zone_sante": zone_sante_param,
            "site": site_param,
            "coordinateur": coordinateur,
            "gestionnaire": gestionnaire_param,
            "sous_mecanisme": sous_mecanisme_param,
            "date_debut": date_debut_param,
            "date_fin": date_fin.strftime("%Y-%m-%d") if date_fin else None,
        }
        cache_key = build_cache_key("dashboard_cache", cache_params)
        cached = cache.get(cache_key)
        
        if cached:
            return Response(cached, status=status.HTTP_200_OK)

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
            coordonnees_sites = coordonnees_sites.filter(
                gestionnaire_site=gestionnaire_param
            )
        if sous_mecanisme_param and sous_mecanisme_param in ["0", "1"]:
            sous_mecanisme = True if sous_mecanisme_param == "1" else False
            mouvements = mouvements.filter(sous_mecanisme=sous_mecanisme)
            coordonnees_sites = coordonnees_sites.filter(sous_mecanisme=sous_mecanisme)
        # if date_debut_param:
        #     date_debut = datetime.strptime(date_debut_param, "%Y-%m-%d").date().replace(day=1)
        #     mouvements = mouvements.filter(date_enregistrement__gte=date_debut)
        if date_fin_param:
            date_fin = datetime.strptime(date_fin_param, "%Y-%m-%d").date()
            dernier_jour_mois = (
                date_fin.replace(day=1)
                + relativedelta(months=1, day=1)
                - timedelta(days=1)
            )

            mouvements = mouvements.filter(date_enregistrement__lte=dernier_jour_mois)

        # Initialisation des variables
        hommes = femmes = personnes_vivant_avec_handicaps = menages = entrees = (
            sorties
        ) = 0
        enfants = adultes = personnes_agees = 0

        # Copie profonde des structures pour éviter les modifications des constantes
        tendances_deplacement_12_mois = [
            dict(mois=m["mois"], annee=date_fin.year, entrees=0, sorties=0)
            for m in MOIS_ANNEE
        ]
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
        par_type_sites = [
            dict(
                type_site=t["type_site"],
                nombre_individus=0,
                nombre_menages=0,
                nombre_sites=0,
            )
            for t in TYPES_SITES
        ]

        coordonnees_sites_serializer = CoordonneesSiteSerializer(
            coordonnees_sites, many=True
        ).data

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
                s["nombre_sites"] = coordonnees_sites.filter(
                    type_site=site_type
                ).count()
                if type_site_mouvement == site_type:
                    if type_mouvement in TYPES_MOUVEMENT_ENTREE:
                        s["nombre_individus"] += m.individus
                        s["nombre_menages"] += m.menage
                    elif type_mouvement in TYPES_MOUVEMENT_SORTIE:
                        s["nombre_individus"] -= m.individus
                        s["nombre_menages"] -= m.menage
                    break

        total_pdi = max(0, entrees - sorties)
        pourcentage_hommes = (
            round((hommes / total_pdi) * 100, 2) if total_pdi != 0 else 0
        )
        pourcentage_femmes = (
            round((femmes / total_pdi) * 100, 2) if total_pdi != 0 else 0
        )
        
        # --- Nettoyage final pour éviter des valeurs < 0 ---
        for tranche in repartition_par_tranche_age:
            tranche["hommes"] = max(0, tranche["hommes"])
            tranche["femmes"] = max(0, tranche["femmes"])
            
        for prov in distribution_par_province_touchees:
            prov["homme"] = max(0, prov["homme"])
            prov["femme"] = max(0, prov["femme"])

        for site in par_type_sites:
            site["nombre_individus"] = max(0, site["nombre_individus"])
            site["nombre_menages"] = max(0, site["nombre_menages"])
            site["nombre_sites"] = max(0, site["nombre_sites"])

        for type_mvt in repartition_par_type_entree:
            type_mvt["nombre"] = max(0, type_mvt["nombre"])

        for type_mvt in repartition_par_type_sortie:
            type_mvt["nombre"] = max(0, type_mvt["nombre"])

        for mois_data in tendances_deplacement_12_mois:
            mois_data["entrees"] = max(0, mois_data["entrees"])
            mois_data["sorties"] = max(0, mois_data["sorties"])
            
        if personnes_vivant_avec_handicaps <= 0:
            # On prends 7% de total pdi en entier
            personnes_vivant_avec_handicaps = round(total_pdi * 0.07)
        
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
                "date_debut": date_debut_param,
                "date_fin": date_fin_param,
            },
            "profil_demographique": {
                "general": {
                    "total_pdi": max(0, total_pdi),
                    "hommes": max(0, hommes),
                    "femmes": max(0, femmes),
                    "pourcentage_hommes": pourcentage_hommes,
                    "pourcentage_femmes": pourcentage_femmes,
                    "personnes_vivant_avec_handicaps": max(
                        0, personnes_vivant_avec_handicaps
                    ),
                    "menages": max(0, menages),
                    "entrees": max(0, entrees),
                    "sorties": max(0, sorties),
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
        
        # --- Mise en cache ---
        cache.set(cache_key, response, CACHE_TIMEOUT)
        
        return Response(response, status=status.HTTP_200_OK)
    except Exception as e:
        return Response(
            {"message": f"Erreur serveur: {str(e)}"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@api_view(["GET"])
def dashboard(request):
    try:
        # --- Récupération des params ---
        province_param = request.GET.get("province")
        territoire_param = request.GET.get("territoire")
        zone_sante_param = request.GET.get("zone_sante")
        site_param = request.GET.get("site")
        coordinateur = request.GET.get("coordinateur")
        gestionnaire_param = request.GET.get("gestionnaire")
        sous_mecanisme_param = request.GET.get("sous_mecanisme")
        date_debut_param = request.GET.get("date_debut")
        date_fin_param = request.GET.get("date_fin")

        # Normalisation des dates
        date_fin = date.today()
        if date_fin_param:
            date_fin = datetime.strptime(date_fin_param, "%Y-%m-%d").date()
            # si tu veux le dernier jour du mois fourni
            date_fin = (date_fin.replace(day=1) + relativedelta(months=1)) - timedelta(
                days=1
            )

        # build cache key
        cache_params = {
            "province": province_param,
            "territoire": territoire_param,
            "zone_sante": zone_sante_param,
            "site": site_param,
            "coordinateur": coordinateur,
            "gestionnaire": gestionnaire_param,
            "sous_mecanisme": sous_mecanisme_param,
            "date_debut": date_debut_param,
            "date_fin": date_fin.strftime("%Y-%m-%d") if date_fin else None,
        }
        cache_key = build_cache_key("dashboard", cache_params)
        cached = cache.get(cache_key)
        
        if cached:
            return Response(cached, status=status.HTTP_200_OK)

        # --- Construire queryset filtré (on évite .all()) ---
        mouvements_qs = MouvementDeplace.objects.order_by("date_enregistrement").filter(
            date_enregistrement__lte=date_fin
        )
        coordonnees_sites_qs = CoordonneesSite.objects.order_by("site_name")
        sites_deplaces = SiteDeplace.objects.order_by("nom_site")
        
        if province_param:
            sites_deplaces = sites_deplaces.filter(province=province_param)
        if territoire_param:
            sites_deplaces = sites_deplaces.filter(
                territoire=territoire_param
            )
        if zone_sante_param:
            sites_deplaces = sites_deplaces.filter(
                zone_sante=zone_sante_param
            )
        if site_param:
            sites_deplaces = sites_deplaces.filter(nom_site=site_param)
        if coordinateur:
            sites_deplaces = sites_deplaces.filter(
                coordinateur=coordinateur
            )
        if gestionnaire_param:
            sites_deplaces = sites_deplaces.filter(
                gestionnaire=gestionnaire_param
            )
        if sous_mecanisme_param in ["0", "1"]:
            sous_mecanisme = sous_mecanisme_param == "1"
            sites_deplaces = sites_deplaces.filter(
                sous_mecanisme=sous_mecanisme
            )
            
        if sites_deplaces.exists():
            mouvements_qs = mouvements_qs.filter(
                site__in=sites_deplaces.values_list("nom_site", flat=True)
            ).distinct()
            coordonnees_sites_qs = coordonnees_sites_qs.filter(
                site_name__in=sites_deplaces.values_list("nom_site", flat=True)
            )
        # date_debut n'est pas utilisé dans ton code original ; garde la porte ouverte
        # if date_debut_param:
        #     date_debut = datetime.strptime(date_debut_param, "%Y-%m-%d").date()
        #     mouvements_qs = mouvements_qs.filter(date_enregistrement__gte=date_debut)
        # if date_fin:
        #     mouvements_qs = mouvements_qs.filter(date_enregistrement__lte=date_fin)

        # --- Pré-calculs : séparons entrées / sorties (SQL) ---
        entrees_qs = mouvements_qs.filter(
            Q(typemouvement__in=TYPES_MOUVEMENT_ENTREE)
            | Q(typemouvement="donnee_brute")
        )
        sorties_qs = mouvements_qs.filter(typemouvement__in=TYPES_MOUVEMENT_SORTIE)

        # Sums globaux (individus, menages, pvh)
        entrees_agg = entrees_qs.aggregate(
            individus_entrees=Sum("individus"),
            menages_entrees=Sum("menage"),
            pvh_entrees=Sum("personne_vivant_handicape"),
        )
        sorties_agg = sorties_qs.aggregate(
            individus_sorties=Sum("individus"),
            menages_sorties=Sum("menage"),
            pvh_sorties=Sum("personne_vivant_handicape"),
        )

        individus_entrees = entrees_agg.get("individus_entrees") or 0
        individus_sorties = sorties_agg.get("individus_sorties") or 0
        menages_entrees = entrees_agg.get("menages_entrees") or 0
        menages_sorties = sorties_agg.get("menages_sorties") or 0
        pvh_entrees = entrees_agg.get("pvh_entrees") or 0
        pvh_sorties = sorties_agg.get("pvh_sorties") or 0

        entrees = individus_entrees
        sorties = individus_sorties
        menages = menages_entrees - menages_sorties
        personnes_vivant_avec_handicaps = pvh_entrees - pvh_sorties

        total_pdi = max(0, entrees - sorties)
        # personnes_vivant_avec_handicaps = max(0, int(total_pdi * 0.07))  # 7% de personnes vivant avec handicaps

        # --- Tranches d'âge : somme par tranche (entrée - sortie) ---
        tranche_fields = {
            "0-4": ("individu_tranche_age_0_4_h", "individu_tranche_age_0_4_f"),
            "5-11": ("individu_tranche_age_5_11_h", "individu_tranche_age_5_11_f"),
            "12-17": ("individu_tranche_age_12_17_h", "individu_tranche_age_12_17_f"),
            "18-24": ("individu_tranche_age_18_24_h", "individu_tranche_age_18_24_f"),
            "25-59": ("individu_tranche_age_25_59_h", "individu_tranche_age_25_59_f"),
            "60+": ("individu_tranche_age_60_h", "individu_tranche_age_60_f"),
        }

        repartition_par_tranche_age = []
        total_hommes = total_femmes = 0
        enfants = adultes = personnes_agees = 0

        for tranche, (hf, ff) in tranche_fields.items():
            e_h = entrees_qs.aggregate(v=Sum(hf)).get("v") or 0
            e_f = entrees_qs.aggregate(v=Sum(ff)).get("v") or 0
            s_h = sorties_qs.aggregate(v=Sum(hf)).get("v") or 0
            s_f = sorties_qs.aggregate(v=Sum(ff)).get("v") or 0

            net_h = (e_h - s_h) or 0
            net_f = (e_f - s_f) or 0

            repartition_par_tranche_age.append(
                {"tranche": tranche, "hommes": net_h, "femmes": net_f}
            )

            total_hommes += net_h
            total_femmes += net_f

            if tranche in ["0-4", "5-11", "12-17"]:
                enfants += net_h + net_f
            elif tranche in ["18-24", "25-59"]:
                adultes += net_h + net_f
            elif tranche == "60+":
                personnes_agees += net_h + net_f

        pourcentage_hommes = (
            round((total_hommes / total_pdi) * 100, 2) if total_pdi else 0
        )
        pourcentage_femmes = (
            round((total_femmes / total_pdi) * 100, 2) if total_pdi else 0
        )

        # --- Répartition par type de mouvement (entrées / sorties) ---
        repartition_par_type_entree = []
        repartition_par_type_sortie = []

        # Entrées
        entr_types = (
            entrees_qs.values("typemouvement")
            .annotate(nombre=Sum("individus"))
            .order_by()
        )
        for t in entr_types:
            repartition_par_type_entree.append(
                {
                    "type_mouvement": t["typemouvement"],
                    "label": t["typemouvement"],
                    "nombre": t["nombre"] or 0,
                }
            )

        # Sorties
        sort_types = (
            sorties_qs.values("typemouvement")
            .annotate(nombre=Sum("individus"))
            .order_by()
        )
        for t in sort_types:
            repartition_par_type_sortie.append(
                {
                    "type_mouvement": t["typemouvement"],
                    "label": t["typemouvement"],
                    "nombre": t["nombre"] or 0,
                }
            )

        # --- Distribution par province urgente (net hommes/femmes par province) ---
        # On somme toutes les tranches en une passe : on groupe par province et somme champs individuels
        # calcule net par province = entrées - sorties
        # Premièrement, on récupère entrées par province
        provinces_entrees = entrees_qs.values("province").annotate(
            homme_entrees=Sum("individu_tranche_age_0_4_h")
            + Sum("individu_tranche_age_5_11_h")
            + Sum("individu_tranche_age_12_17_h")
            + Sum("individu_tranche_age_18_24_h")
            + Sum("individu_tranche_age_25_59_h")
            + Sum("individu_tranche_age_60_h"),
            femme_entrees=Sum("individu_tranche_age_0_4_f")
            + Sum("individu_tranche_age_5_11_f")
            + Sum("individu_tranche_age_12_17_f")
            + Sum("individu_tranche_age_18_24_f")
            + Sum("individu_tranche_age_25_59_f")
            + Sum("individu_tranche_age_60_f"),
        )
        provinces_sorties = sorties_qs.values("province").annotate(
            homme_sorties=Sum("individu_tranche_age_0_4_h")
            + Sum("individu_tranche_age_5_11_h")
            + Sum("individu_tranche_age_12_17_h")
            + Sum("individu_tranche_age_18_24_h")
            + Sum("individu_tranche_age_25_59_h")
            + Sum("individu_tranche_age_60_h"),
            femme_sorties=Sum("individu_tranche_age_0_4_f")
            + Sum("individu_tranche_age_5_11_f")
            + Sum("individu_tranche_age_12_17_f")
            + Sum("individu_tranche_age_18_24_f")
            + Sum("individu_tranche_age_25_59_f")
            + Sum("individu_tranche_age_60_f"),
        )

        # Build maps pour lookup rapide
        pe_map = {
            p["province"]: {
                "homme": p.get("homme_entrees") or 0,
                "femme": p.get("femme_entrees") or 0,
            }
            for p in provinces_entrees
        }
        ps_map = {
            p["province"]: {
                "homme": p.get("homme_sorties") or 0,
                "femme": p.get("femme_sorties") or 0,
            }
            for p in provinces_sorties
        }

        distribution_par_province_touchees = []
        for p in PROVINCES_URGENTS:
            nom = p["province"]
            homme_net = (
                pe_map.get(nom, {}).get("homme", 0)
                - ps_map.get(nom, {}).get("homme", 0)
            ) or 0
            femme_net = (
                pe_map.get(nom, {}).get("femme", 0)
                - ps_map.get(nom, {}).get("femme", 0)
            ) or 0
            distribution_par_province_touchees.append(
                {"province": nom, "homme": homme_net, "femme": femme_net}
            )

        # --- Tendances des 12 derniers mois (par mois) ---
        tendances_deplacement_12_mois = []
        # Initialiser la structure à partir de MOIS_ANNEE (supposée exister)
        for m in MOIS_ANNEE:
            tendances_deplacement_12_mois.append(
                {"mois": m["mois"], "annee": date_fin.year, "entrees": 0, "sorties": 0}
            )

        tendances_qs = (
            mouvements_qs.annotate(
                mois=ExtractMonth("date_enregistrement"),
                annee=ExtractYear("date_enregistrement"),
            )
            .values("mois", "annee", "typemouvement")
            .annotate(total=Sum("individus"))
        )

        # remplir la structure
        for t in tendances_qs:
            mois = t["mois"]
            annee = t["annee"]
            typ = t["typemouvement"]
            total = t["total"] or 0
            # rechercher entrée correspondante dans tendances_deplacement_12_mois
            for md in tendances_deplacement_12_mois:
                if md["mois"] == mois and md["annee"] == annee:
                    if typ in TYPES_MOUVEMENT_ENTREE or typ == "donnee_brute":
                        md["entrees"] += total
                    elif typ in TYPES_MOUVEMENT_SORTIE:
                        md["sorties"] += total
                    break

        # --- Par type de site : nombre sites (coordonnees_sites) + individus/menages net ---
        sites_counts = coordonnees_sites_qs.values("type_site").annotate(
            nombre_sites=Count("id")
        )
        sites_count_map = {s["type_site"]: s["nombre_sites"] for s in sites_counts}

        # mouvements par type_site (net individus et menages)
        entrees_par_type_site = entrees_qs.values("type_site").annotate(
            individus=Sum("individus"), menages=Sum("menage")
        )
        sorties_par_type_site = sorties_qs.values("type_site").annotate(
            individus=Sum("individus"), menages=Sum("menage")
        )
        e_map = {
            e["type_site"]: {
                "individus": e.get("individus") or 0,
                "menages": e.get("menages") or 0,
            }
            for e in entrees_par_type_site
        }
        s_map = {
            s["type_site"]: {
                "individus": s.get("individus") or 0,
                "menages": s.get("menages") or 0,
            }
            for s in sorties_par_type_site
        }

        par_type_sites = []
        for t in TYPES_SITES:
            type_name = t["type_site"]
            nb_sites = sites_count_map.get(type_name, 0)
            individus_net = (
                e_map.get(type_name, {}).get("individus", 0)
                - s_map.get(type_name, {}).get("individus", 0)
            ) or 0
            menages_net = (
                e_map.get(type_name, {}).get("menages", 0)
                - s_map.get(type_name, {}).get("menages", 0)
            ) or 0
            par_type_sites.append(
                {
                    "type_site": type_name,
                    "nombre_individus": individus_net,
                    "nombre_menages": menages_net,
                    "nombre_sites": nb_sites,
                }
            )

        # --- Serializer pour coordonnees_sites (filtré) ---
        coordonnees_sites_serializer = CoordonneesSiteSerializer(
            coordonnees_sites_qs, many=True
        ).data

        # --- Construction de la réponse ---
        response = {
            "params": cache_params,
            "profil_demographique": {
                "general": {
                    "total_pdi": total_pdi,
                    "hommes": max(0, total_hommes),
                    "femmes": max(0, total_femmes),
                    "pourcentage_hommes": pourcentage_hommes,
                    "pourcentage_femmes": pourcentage_femmes,
                    "personnes_vivant_avec_handicaps": max(
                        0, personnes_vivant_avec_handicaps
                    ),
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
                "par_type_mouvement": repartition_par_type_entree
                + repartition_par_type_sortie,
            },
            "tendances_deplacement_12_mois": tendances_deplacement_12_mois,
            "coordonnees_sites": coordonnees_sites_serializer,
        }

        # --- Mise en cache ---
        cache.set(cache_key, response, CACHE_TIMEOUT)

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
