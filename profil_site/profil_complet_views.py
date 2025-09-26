from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from utils.choices import *
from utils.functions import convert_to_date

from .customs_models.bases.profil_site import ProfilSite, ProfilSiteSerializer, FormProfilSiteSerializer

from .customs_models.autres.gestion_admin_site import GestionAdminProfilSite, GestionAdminProfilSiteSerializer
from .customs_models.autres.gouvernance_participation_site import OrganisationInterneFonctionnementProfilSite, OrganisationInterneFonctionnementProfilSiteSerializer
from .customs_models.autres.moyens_subsistance_besoins_prioritaires import MoyenSubsistanceBesoinPrioritaireProfilSite, MoyenSubsistanceBesoinPrioritaireProfilSiteSerializer
from .customs_models.autres.vulnerabilite_site import VulnerabilitePopulationProfilSite, VulnerabilitePopulationProfilSiteSerializer

from .customs_models.secteurs.abris_ames_site import AbrisAmesProfilSite, AbrisAmesProfilSiteSerializer
from .customs_models.secteurs.cartographie_service_acteurs import CartographieServiceActeurProfilSite, CartographieServiceActeurProfilSiteSerializer
from .customs_models.secteurs.eduction import EducationProfilSite, EducationProfilSiteSerializer
from .customs_models.secteurs.protection import ProtectionProfilSite, ProtectionProfilSiteSerializer
from .customs_models.secteurs.sante_site import SanteProfilSite, SanteProfilSiteSerializer
from .customs_models.secteurs.securite_alimentaire import SecuriteAlimentaireProfilSite, SecuriteAlimentaireProfilSiteSerializer
from .customs_models.secteurs.wash_site import WashProfilSite, WashProfilSiteSerializer

# PROFIL DE SITE COMPLET

def api_response(success, message, data=None):
    return {
        'success': success,
        'message': message,
        'data': data
    }

@api_view(['GET'])
def options_choices(request):
    try:
        options = {
            "TYPE_SITE_OPTIONS": TYPE_SITE_OPTIONS,
            "TYPE_PROPRIETE_FONCIERE_OPTIONS": TYPE_PROPRIETE_FONCIERE_OPTIONS,
            "TYPE_INSTALLATION_OPTIONS": TYPE_INSTALLATION_OPTIONS,
            "STATUT_SITE_OPTIONS": STATUT_SITE_OPTIONS,
            "OUI_NON_OPTIONS": OUI_NON_OPTIONS,
            "SEXE_OPTIONS": SEXE_OPTIONS,
            "COMITES_OPTIONS": COMITES_OPTIONS,
            "ETAT_COMITES_OPTIONS": ETAT_COMITES_OPTIONS,
            "OUI_PARTIELLEMENT_NON_OPTIONS": OUI_PARTIELLEMENT_NON_OPTIONS,
            "MOYENS_COMMINICATION_DISTRIBUTION_OPTIONS": MOYENS_COMMINICATION_DISTRIBUTION_OPTIONS,
            "RAISONS_RETOURS_OPTIONS": RAISONS_RETOURS_OPTIONS,
            "TYPE_ABRIS_OPTIONS": TYPE_ABRIS_OPTIONS,
            "AME_BASE_CHOICES": AME_BASE_CHOICES,
            "AME_SAISON_SECHE_CHOICES": AME_SAISON_SECHE_CHOICES,
            "STATEGIES_COURANTES_MANQUE_AME_OPTIONS": STATEGIES_COURANTES_MANQUE_AME_OPTIONS,
            "ETAT_GENERAL_PARCELLES_ROUTES_CANIVEAUX_OPTIONS": ETAT_GENERAL_PARCELLES_ROUTES_CANIVEAUX_OPTIONS,
            "SOURCES_PRINCIPALES_ELECTRICITE_OPTIONS": SOURCES_PRINCIPALES_ELECTRICITE_OPTIONS,
            "SOURCE_PRINCIPALE_EAU_POTABLE_OPTIONS": SOURCE_PRINCIPALE_EAU_POTABLE_OPTIONS,
            "METHODES_ELIMINATION_DECHET_OPTIONS": METHODES_ELIMINATION_DECHET_OPTIONS,
            "TYPES_LATRINES_DOUCHES_OPTIONS": TYPES_LATRINES_DOUCHES_OPTIONS,
            "PROBLEMES_SANTE_RESIDENTS_OPTIONS": PROBLEMES_SANTE_RESIDENTS_OPTIONS,
            "PROBLEMES_FAMILLES_ACCES_SOINS_OPTIONS": PROBLEMES_FAMILLES_ACCES_SOINS_OPTIONS,
            "NOMBRE_REPAS_PAR_JOUR_OPTIONS": NOMBRE_REPAS_PAR_JOUR_OPTIONS,
            "DIFFICULTES_ACCES_NOURRITURE": DIFFICULTES_ACCES_NOURRITURE,
            "FREQUENCE_AIDES_ALIMENTAIRE_OPTIONS": FREQUENCE_AIDES_ALIMENTAIRE_OPTIONS,
            "RESTRICTIONS_MOUVEMENT_OPTIONS": RESTRICTIONS_MOUVEMENT_OPTIONS,
            "ACTEURS_INCIDENTS_IMPLIQUES_OPTIONS": ACTEURS_INCIDENTS_IMPLIQUES_OPTIONS,
            "MENANCES_COURANTES_OPTIONS": MENANCES_COURANTES_OPTIONS,
            "ZONES_INSECURES_OPTIONS": ZONES_INSECURES_OPTIONS,
            "TYPES_SERVICES_SOUTIEN_PSYCHOSOCIAL_OPTIONS": TYPES_SERVICES_SOUTIEN_PSYCHOSOCIAL_OPTIONS,
            "PRINCIPALES_OBSTACLES_ACCES_EDUCTIONS": PRINCIPALES_OBSTACLES_ACCES_EDUCTIONS,
            "ARTICLES_BESOIN_EXISTANT_MARCHE_OPTIONS": ARTICLES_BESOIN_EXISTANT_MARCHE_OPTIONS,
            "PRINCIPAUX_MOYENS_SUBSISTANCE_OPTIONS": PRINCIPAUX_MOYENS_SUBSISTANCE_OPTIONS,
            "BESOINS_PRIORITAIRES_OPTIONS": BESOINS_PRIORITAIRES_OPTIONS,
            "ETAT_SERVICES_OPTIONS": ETAT_SERVICES_OPTIONS,
        }
        response = api_response(True, "Options chargées avec succès", options)
        return Response(response, status=status.HTTP_200_OK)
    except Exception as e:
        response = api_response(False, "Un probleme est survenu, veuillez reessayer plus tard")
        return Response(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
@api_view(['GET'])
def profils_sites_complet(request, id=None):
    try:
        if id:
            profil = ProfilSite.objects.get(id=id)
            serializer = ProfilSiteSerializer(profil).data

            site = profil.site
            sections = {
                "gestion_administration": (GestionAdminProfilSite, GestionAdminProfilSiteSerializer),
                "organisation_fonctionnement": (OrganisationInterneFonctionnementProfilSite, OrganisationInterneFonctionnementProfilSiteSerializer),
                "vulnerabilites": (VulnerabilitePopulationProfilSite, VulnerabilitePopulationProfilSiteSerializer),
                "abris_ame": (AbrisAmesProfilSite, AbrisAmesProfilSiteSerializer),
                "wash": (WashProfilSite, WashProfilSiteSerializer),
                "sante": (SanteProfilSite, SanteProfilSiteSerializer),
                "securite_alimentaire": (SecuriteAlimentaireProfilSite, SecuriteAlimentaireProfilSiteSerializer),
                "protection": (ProtectionProfilSite, ProtectionProfilSiteSerializer),
                "education": (EducationProfilSite, EducationProfilSiteSerializer),
                "moyens_subsistance": (MoyenSubsistanceBesoinPrioritaireProfilSite, MoyenSubsistanceBesoinPrioritaireProfilSiteSerializer),
                "cartographie_acteurs_services": (CartographieServiceActeurProfilSite, CartographieServiceActeurProfilSiteSerializer),
            }

            for key, (model, serializer_class) in sections.items():
                obj = model.objects.filter(site=site).order_by('-created_at').first()
                serializer[key] = serializer_class(obj).data if obj else None
                
            response = api_response(
                True,
                f"Profil du site {profil.site.nom_site} chargé avec succès",
                serializer
            )

            return Response(response, status=status.HTTP_200_OK)

        # Liste de profils
        profils_site = ProfilSite.objects.all().order_by('-created_at')

        site_code = request.GET.get('site_code', "").strip()
        date_debut = request.GET.get('date_debut', "").strip()
        date_fin = request.GET.get('date_fin', "").strip()

        if site_code:
            profils_site = profils_site.filter(site__code_site=site_code)

        if date_debut or date_fin:
            if date_debut:
                date_debut = convert_to_date(date_debut)
            if date_fin:
                date_fin = convert_to_date(date_fin)

            if date_debut and date_fin:
                profils_site = profils_site.filter(created_at__range=[date_debut, date_fin])
            elif date_debut:
                profils_site = profils_site.filter(created_at__gte=date_debut)
            elif date_fin:
                profils_site = profils_site.filter(created_at__lte=date_fin)

        serializer = ProfilSiteSerializer(profils_site, many=True).data
        
        response = api_response(
            True, "Liste des profils chargé avec succés", serializer
        )
        return Response(response, status=status.HTTP_200_OK)

    except ProfilSite.DoesNotExist:
        response = api_response(
            False, "Profil du site n'existe pas",
        )
        return Response(response, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        response = api_response(
            False, "Un probleme est survenu, veuillez reessayer plus tard",
        )
        return Response(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

# Fonction utilitaire générique
def handle_create(request, serializer_class, success_message):
    try:
        serializer = serializer_class(data=request.data)
        if serializer.is_valid():
            obj = serializer.save()
            response = api_response(True, success_message, serializer_class(obj).data)
            return Response(response, status=status.HTTP_201_CREATED)
        response = api_response(False, "Un problème est survenu, veuillez réessayer plus tard", serializer.errors)
        return Response(response, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        response = api_response(False, "Un problème est survenu, veuillez réessayer plus tard")
        return Response(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# Ensuite tu crées des petites vues wrappers ultra-légères

@api_view(['POST', 'PUT'])
def create_profil_site(request):
    return handle_create(request, FormProfilSiteSerializer, "Profil du site créé avec succès")

@api_view(['POST', 'PUT'])
def create_gestion_administration_profil_site(request):
    return handle_create(request, GestionAdminProfilSiteSerializer, "Gestion de l'administration créée avec succès")

@api_view(['POST', 'PUT'])
def create_organisation_fonctionnement_profil_site(request):
    return handle_create(request, OrganisationInterneFonctionnementProfilSiteSerializer, "Organisation interne de fonctionnement créée avec succès")

@api_view(['POST', 'PUT'])
def create_vulnerabilites_profil_site(request):
    return handle_create(request, VulnerabilitePopulationProfilSiteSerializer, "Vulnérabilités de la population créées avec succès")

@api_view(['POST', 'PUT'])
def create_abris_ame_profil_site(request):
    return handle_create(request, AbrisAmesProfilSiteSerializer, "Abris/AME créé avec succès")

@api_view(['POST', 'PUT'])
def create_wash_profil_site(request):
    return handle_create(request, WashProfilSiteSerializer, "Wash créé avec succès")

@api_view(['POST', 'PUT'])
def create_sante_profil_site(request):
    return handle_create(request, SanteProfilSiteSerializer, "Santé créée avec succès")

@api_view(['POST', 'PUT'])
def create_securite_alimentaire_profil_site(request):
    return handle_create(request, SecuriteAlimentaireProfilSiteSerializer, "Sécurité alimentaire créée avec succès")

@api_view(['POST', 'PUT'])
def create_protection_profil_site(request):
    return handle_create(request, ProtectionProfilSiteSerializer, "Protection créée avec succès")

@api_view(['POST', 'PUT'])
def create_education_profil_site(request):
    return handle_create(request, EducationProfilSiteSerializer, "Éducation créée avec succès")

@api_view(['POST', 'PUT'])
def create_moyens_subsistance_profil_site(request):
    return handle_create(request, MoyenSubsistanceBesoinPrioritaireProfilSiteSerializer, "Moyens de subsistance créés avec succès")

@api_view(['POST', 'PUT'])
def create_cartographie_acteurs_services_profil_site(request):
    return handle_create(request, CartographieServiceActeurProfilSiteSerializer, "Cartographie des acteurs et services créée avec succès")