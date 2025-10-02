from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import ValidationError

from utils.choices import *
from utils.functions import convert_to_date

from data_import.models import SiteDeplace
from data_import.serializers import SiteDeplaceSerializer
from .customs_models.bases.profil_site import (
    ProfilSite,
    ProfilSiteSerializer,
    FormProfilSiteSerializer,
)

from .customs_models.autres.gestion_admin_site import (
    GestionAdminProfilSite,
    GestionAdminProfilSiteSerializer,
    FormGestionAdminProfilSiteSerializer,
)
from .customs_models.autres.gouvernance_participation_site import (
    OrganisationInterneFonctionnementProfilSite,
    OrganisationInterneFonctionnementProfilSiteSerializer,
    FormOrganisationInterneFonctionnementProfilSiteSerializer,
)
from .customs_models.autres.moyens_subsistance_besoins_prioritaires import (
    MoyenSubsistanceBesoinPrioritaireProfilSite,
    MoyenSubsistanceBesoinPrioritaireProfilSiteSerializer,
    FormMoyenSubsistanceBesoinPrioritaireProfilSiteSerializer,
)
from .customs_models.autres.vulnerabilite_site import (
    VulnerabilitePopulationProfilSite,
    VulnerabilitePopulationProfilSiteSerializer,
    FormVulnerabilitePopulationProfilSiteSerializer,
)

from .customs_models.secteurs.abris_ames_site import (
    AbrisAmesProfilSite,
    AbrisAmesProfilSiteSerializer,
    FormAbrisAmesProfilSiteSerializer,
)
from .customs_models.secteurs.cartographie_service_acteurs import (
    CartographieServiceActeurProfilSite,
    CartographieServiceActeurProfilSiteSerializer,
    FormCartographieServiceActeurProfilSiteSerializer,
)
from .customs_models.secteurs.eduction import (
    EducationProfilSite,
    EducationProfilSiteSerializer,
    FormEducationProfilSiteSerializer,
)
from .customs_models.secteurs.protection import (
    ProtectionProfilSite,
    ProtectionProfilSiteSerializer,
    FormProtectionProfilSiteSerializer,
)
from .customs_models.secteurs.sante_site import (
    SanteProfilSite,
    SanteProfilSiteSerializer,
    FormSanteProfilSiteSerializer,
)
from .customs_models.secteurs.securite_alimentaire import (
    SecuriteAlimentaireProfilSite,
    SecuriteAlimentaireProfilSiteSerializer,
    FormSecuriteAlimentaireProfilSiteSerializer,
)
from .customs_models.secteurs.wash_site import (
    WashProfilSite,
    WashProfilSiteSerializer,
    FormWashProfilSiteSerializer,
)


def api_response(success, message, data=None):
    return {"success": success, "message": message, "data": data}


# PROFIL DE SITE COMPLET


@api_view(["GET"])
def sites_deplaces(request, id=None):
    try:
        if id:
            site = SiteDeplace.objects.get(id=id)
            serializer = SiteDeplaceSerializer(site)
            response = api_response(
                success=True,
                message="Site deplacé récupéré avec succès",
                data=serializer.data,
            )
            return Response(response, status=status.HTTP_200_OK)
        else:
            sites = SiteDeplace.objects.all().order_by("nom_site")
            serializer = SiteDeplaceSerializer(sites, many=True)
            response = api_response(
                success=True,
                message="Sites deplacés récupérés avec succès",
                data=serializer.data,
            )
            return Response(response, status=status.HTTP_200_OK)
    except SiteDeplace.DoesNotExist:
        response = api_response(
            success=False, message="Site deplacé n'existe pas", data=None
        )
        return Response(response, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        response = api_response(success=False, message=str(e), data=None)
        return Response(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["GET"])
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
            # "NOMBRE_REPAS_PAR_JOUR_OPTIONS": NOMBRE_REPAS_PAR_JOUR_OPTIONS,
            "DIFFICULTES_ACCES_NOURRITURE": DIFFICULTES_ACCES_NOURRITURE,
            "FREQUENCE_AIDES_ALIMENTAIRE_OPTIONS": FREQUENCE_AIDES_ALIMENTAIRE_OPTIONS,
            "RESTRICTIONS_MOUVEMENT_OPTIONS": RESTRICTIONS_MOUVEMENT_OPTIONS,
            "OUI_NON_JE_PREFERE_NON_REPONDRE": OUI_NON_JE_PREFERE_NON_REPONDRE,
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
        response = api_response(
            False, "Un probleme est survenu, veuillez reessayer plus tard"
        )
        return Response(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
@api_view(["GET"])
def get_profil_site_by_code(request, code_site: str):
    try:
        profil = ProfilSite.objects.filter(site__code_site=code_site).order_by("-created_at").first()
        if not profil:
            response = api_response(
                False,
                f"Aucun profil trouvé pour le site avec le code '{code_site}'.",
            )
            return Response(response, status=status.HTTP_404_NOT_FOUND)
        
        serializer = ProfilSiteSerializer(profil).data

        site = profil.site
        sections = {
            "gestion_administration": (
                GestionAdminProfilSite,
                GestionAdminProfilSiteSerializer,
            ),
            "organisation_fonctionnement": (
                OrganisationInterneFonctionnementProfilSite,
                OrganisationInterneFonctionnementProfilSiteSerializer,
            ),
            "vulnerabilites": (
                VulnerabilitePopulationProfilSite,
                VulnerabilitePopulationProfilSiteSerializer,
            ),
            "abris_ame": (AbrisAmesProfilSite, AbrisAmesProfilSiteSerializer),
            "wash": (WashProfilSite, WashProfilSiteSerializer),
            "sante": (SanteProfilSite, SanteProfilSiteSerializer),
            "securite_alimentaire": (
                SecuriteAlimentaireProfilSite,
                SecuriteAlimentaireProfilSiteSerializer,
            ),
            "protection": (ProtectionProfilSite, ProtectionProfilSiteSerializer),
            "education": (EducationProfilSite, EducationProfilSiteSerializer),
            "moyens_subsistance": (
                MoyenSubsistanceBesoinPrioritaireProfilSite,
                MoyenSubsistanceBesoinPrioritaireProfilSiteSerializer,
            ),
            "cartographie_acteurs_services": (
                CartographieServiceActeurProfilSite,
                CartographieServiceActeurProfilSiteSerializer,
            ),
        }

        for key, (model, serializer_class) in sections.items():
            obj = model.objects.filter(site=site).order_by("-created_at").first()
            serializer[key] = serializer_class(obj).data if obj else None

        response = api_response(
            True,
            f"Profil du site {profil.site.nom_site} chargé avec succès",
            serializer,
        )
        return Response(response, status=status.HTTP_200_OK)
    except Exception as e:
        response = api_response(
            False, "Un probleme est survenu, veuillez reessayer plus tard"
        )
        return Response(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["GET"])
def profils_sites_complet(request, id=None):
    try:
        if id:
            profil = ProfilSite.objects.get(id=id)
            serializer = ProfilSiteSerializer(profil).data

            site = profil.site
            sections = {
                "gestion_administration": (
                    GestionAdminProfilSite,
                    GestionAdminProfilSiteSerializer,
                ),
                "organisation_fonctionnement": (
                    OrganisationInterneFonctionnementProfilSite,
                    OrganisationInterneFonctionnementProfilSiteSerializer,
                ),
                "vulnerabilites": (
                    VulnerabilitePopulationProfilSite,
                    VulnerabilitePopulationProfilSiteSerializer,
                ),
                "abris_ame": (AbrisAmesProfilSite, AbrisAmesProfilSiteSerializer),
                "wash": (WashProfilSite, WashProfilSiteSerializer),
                "sante": (SanteProfilSite, SanteProfilSiteSerializer),
                "securite_alimentaire": (
                    SecuriteAlimentaireProfilSite,
                    SecuriteAlimentaireProfilSiteSerializer,
                ),
                "protection": (ProtectionProfilSite, ProtectionProfilSiteSerializer),
                "education": (EducationProfilSite, EducationProfilSiteSerializer),
                "moyens_subsistance": (
                    MoyenSubsistanceBesoinPrioritaireProfilSite,
                    MoyenSubsistanceBesoinPrioritaireProfilSiteSerializer,
                ),
                "cartographie_acteurs_services": (
                    CartographieServiceActeurProfilSite,
                    CartographieServiceActeurProfilSiteSerializer,
                ),
            }

            for key, (model, serializer_class) in sections.items():
                obj = model.objects.filter(site=site).order_by("-created_at").first()
                serializer[key] = serializer_class(obj).data if obj else None

            response = api_response(
                True,
                f"Profil du site {profil.site.nom_site} chargé avec succès",
                serializer,
            )

            return Response(response, status=status.HTTP_200_OK)

        # Liste de profils sites
        profils_site = ProfilSite.objects.all().order_by("-created_at")

        site_code = request.GET.get("site_code", "").strip()
        date_debut = request.GET.get("date_debut", "").strip()
        date_fin = request.GET.get("date_fin", "").strip()

        if site_code:
            profils_site = profils_site.filter(site__code_site=site_code)

        if date_debut or date_fin:
            if date_debut:
                date_debut = convert_to_date(date_debut)
            if date_fin:
                date_fin = convert_to_date(date_fin)

            if date_debut and date_fin:
                profils_site = profils_site.filter(
                    created_at__range=[date_debut, date_fin]
                )
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
            False,
            "Profil du site n'existe pas",
        )
        return Response(response, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        response = api_response(
            False,
            "Un probleme est survenu, veuillez reessayer plus tard",
        )
        return Response(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# Fonction utilitaire générique
def handle_create(request, form_serializer_class, success_message, response_serializer=None):
    try:
        serializer = form_serializer_class(data=request.data)
        if serializer.is_valid():
            obj = serializer.save()
            response = api_response(
                True,
                success_message,
                (
                    response_serializer(obj).data
                    if response_serializer
                    else form_serializer_class(obj).data
                ),
            )
            return Response(response, status=status.HTTP_201_CREATED)
        response = api_response(
            False, "Un erreur est survenu lors de la création", serializer.errors
        )
        return Response(response, status=status.HTTP_400_BAD_REQUEST)
    except ValidationError as e:
        # Ici on renvoie les erreurs de validation
        response = api_response(
            False, "Un erreur est survenu lors de la création", e.detail
        )
        return Response(response, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        print(f"Error --> {e}")
        response = api_response(
            False, "Un problème est survenu, veuillez réessayer plus tard"
        )
        return Response(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# Ensuite tu crées des petites vues wrappers ultra-légères


@api_view(["POST", "PUT"])
def create_profil_site(request):
    return handle_create(
        request,
        FormProfilSiteSerializer,
        "Profil du site créé avec succès",
        ProfilSiteSerializer,
    )


@api_view(["POST", "PUT"])
def create_gestion_administration_profil_site(request):
    return handle_create(
        request,
        FormGestionAdminProfilSiteSerializer,
        "Gestion de l'administration créée avec succès",
        GestionAdminProfilSiteSerializer,
    )


@api_view(["POST", "PUT"])
def create_organisation_fonctionnement_profil_site(request):
    return handle_create(
        request,
        FormOrganisationInterneFonctionnementProfilSiteSerializer,
        "Organisation interne de fonctionnement créée avec succès",
        OrganisationInterneFonctionnementProfilSiteSerializer,
    )


@api_view(["POST", "PUT"])
def create_vulnerabilites_profil_site(request):
    return handle_create(
        request,
        FormVulnerabilitePopulationProfilSiteSerializer,
        "Vulnérabilités de la population créées avec succès",
        VulnerabilitePopulationProfilSiteSerializer,
    )


@api_view(["POST", "PUT"])
def create_abris_ame_profil_site(request):
    return handle_create(
        request,
        FormAbrisAmesProfilSiteSerializer,
        "Abris/AME créé avec succès",
        AbrisAmesProfilSiteSerializer,
    )


@api_view(["POST", "PUT"])
def create_wash_profil_site(request):
    return handle_create(
        request,
        FormWashProfilSiteSerializer,
        "Wash créé avec succès",
        WashProfilSiteSerializer,
    )


@api_view(["POST", "PUT"])
def create_sante_profil_site(request):
    return handle_create(
        request,
        FormSanteProfilSiteSerializer,
        "Santé créée avec succès",
        SanteProfilSiteSerializer,
    )


@api_view(["POST", "PUT"])
def create_securite_alimentaire_profil_site(request):
    return handle_create(
        request,
        FormSecuriteAlimentaireProfilSiteSerializer,
        "Sécurité alimentaire créée avec succès",
        SecuriteAlimentaireProfilSiteSerializer,
    )


@api_view(["POST", "PUT"])
def create_protection_profil_site(request):
    return handle_create(
        request, 
        FormProtectionProfilSiteSerializer,
        "Protection créée avec succès",
        ProtectionProfilSiteSerializer, 
    )


@api_view(["POST", "PUT"])
def create_education_profil_site(request):
    return handle_create(
        request, 
        FormEducationProfilSiteSerializer,
        "Éducation créée avec succès",
        EducationProfilSiteSerializer, 
    )


@api_view(["POST", "PUT"])
def create_moyens_subsistance_profil_site(request):
    return handle_create(
        request,
        FormMoyenSubsistanceBesoinPrioritaireProfilSiteSerializer,
        "Moyens de subsistance créés avec succès",
        MoyenSubsistanceBesoinPrioritaireProfilSiteSerializer,
    )


@api_view(["POST", "PUT"])
def create_cartographie_acteurs_services_profil_site(request):
    return handle_create(
        request,
        FormCartographieServiceActeurProfilSiteSerializer,
        "Cartographie des acteurs et services créée avec succès",
        CartographieServiceActeurProfilSiteSerializer,
    )
