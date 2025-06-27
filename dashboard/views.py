from rest_framework.response import Response
from rest_framework import status
from .models import *
from datetime import date

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

TYPES_MOUVEMENT = [
    {"type_mouvement": "naissance", "label": "Naissance", "nombre": 0},
    {"type_mouvement": "reunification", "label": "Reunification", "nombre": 0},
    {"type_mouvement": "entree", "label": "Entrée", "nombre": 0},
    {"type_mouvement": "deces", "label": "Décès", "nombre": 0},
    {"type_mouvement": "sortie", "label": "Sortie", "nombre": 0},
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
    {"type_site": "Site Planifie", "nombre": 0},
    {"type_site": "Site Spontane", "nombre": 0},
    {"type_site": "Centre Collectif", "nombre": 0},
]


def dashboard(request):
    try:
        mouvemets = MouvementDeplace.objects.all()
        province_param = request.GET.get("province")
        territoire_param = request.GET.get("territoire")
        zone_sante_param = request.GET.get("zone_sante")
        site_param = request.GET.get("site")
        coordinateur = request.GET.get("coordinateur")
        gestionnaire_param = request.GET.get("gestionnaire")
        sous_mecanisme_param = request.GET.get("sous_mecanisme")
        deadline_param = request.GET.get("deadline")

        par_type_sites = []

        total_pdi = 0
        hommes = 0
        femmes = 0
        personnes_vivant_avec_handicaps = 0

        menages = 0
        entrees = 0
        sorties = 0

        repartition_par_tranche_age = []
        distribution_par_province_touchees = []
        tendances_deplacement_12_mois = []
        repartition_par_type_entree = []
        repartition_par_type_sortie = []
        coordonnees_sites = []

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
                    "hommes": hommes,
                    "femmes": femmes,
                    "personnes_vivant_avec_handicaps": personnes_vivant_avec_handicaps,
                    "menages": menages,
                    "entrees": entrees,
                    "sorties": sorties,
                },
                "par_type_sites": par_type_sites,
                "repartition_par_tranche_age": repartition_par_tranche_age,
                "distribution_par_province_touchees": distribution_par_province_touchees,
                "tendances_deplacement_12_mois": tendances_deplacement_12_mois,
                "repartition_par_type_entree": repartition_par_type_entree,
                "repartition_par_type_sortie": repartition_par_type_sortie,
                "coordonnees_sites": coordonnees_sites,
            },
        }
        return Response(response, status=status.HTTP_200_OK)
    except Exception as e:
        return Response(
            {"message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
