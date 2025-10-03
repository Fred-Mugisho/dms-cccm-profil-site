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
import logging

logger = logging.getLogger(__name__)

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
    
@api_view(["POST", "PUT", "GET", "DELETE"])
def charger_data_profil_site(request):
    try:
        from .data import DATA
        # data = request.data
        logger.info(f"Loading data...")
        for item in DATA:
            code_site = item.get("code_site")
            logger.info(f"Processing item: {code_site}")
            site_with_code = SiteDeplace.objects.filter(code_site=code_site).first()
            if not site_with_code:
                logger.error(f"Aucun site trouvé avec le code '{code_site}'.")
                continue
            
            profil_data = {
                "code_site": site_with_code.code_site,
                "enqueteur": item.get("enqueteur", None),
                "organisation": item.get("organisation", None),
                "nombre_menages": item.get("nombre_menages", None),
                "nombre_individus": item.get("nombre_individus", None),
                "individus_0_4_f": item.get("individus_0_4_f", 0) or 0,
                "individus_5_11_f": item.get("individus_5_11_f", 0) or 0,
                "individus_12_17_f": item.get("individus_12_17_f", 0) or 0,
                "individus_18_24_f": item.get("individus_18_24_f", 0) or 0,
                "individus_25_59_f": item.get("individus_25_59_f", 0) or 0,
                "individus_60_f": item.get("individus_60_f", 0) or 0,
                "individus_0_4_h": item.get("individus_0_4_h", 0) or 0,
                "individus_5_11_h": item.get("individus_5_11_h", 0) or 0,
                "individus_12_17_h": item.get("individus_12_17_h", 0) or 0,
                "individus_18_24_h": item.get("individus_18_24_h", 0) or 0,
                "individus_25_59_h": item.get("individus_25_59_h", 0) or 0,
                "individus_60_h": item.get("individus_60_h", 0) or 0,
                "statut_site": item.get("statut_site", None),
            }
            gestion_administration_data = item.get("gestion_administration", {})
            organisation_fonctionnement_data = item.get("organisation_fonctionnement", {})
            vulnerabilites_data = item.get("vulnerabilites", {})
            abris_ame_data = item.get("abris_ame", {})
            wash_data = item.get("wash", {})
            sante_data = item.get("sante", {})
            securite_alimentaire_data = item.get("securite_alimentaire", {})
            protection_data = item.get("protection", {})
            education_data = item.get("education", {})
            moyens_subsistance_data = item.get("moyens_subsistance", {})
            cartographie_acteurs_services_data = item.get("cartographie_acteurs_services", {})
            
            logger.info(f"Creating profil for site: {code_site}")
            
            profil_serializer = FormProfilSiteSerializer(data=profil_data)
            if profil_serializer.is_valid():
                profil_serializer.save()
                
                logger.info(f"Saved profil for site: {code_site}")
                
                if gestion_administration_data:
                    gestion_administration_data["code_site"] = code_site
                    gestion_serializer = FormGestionAdminProfilSiteSerializer(data=gestion_administration_data)
                    if gestion_serializer.is_valid():
                        gestion_serializer.save()
                        logger.info(f"Saved gestion_administration for site: {code_site}")
                    else:
                        logger.error(f"Erreur de validation pour gestion_administration du site '{code_site}': {gestion_serializer.errors}")
                        return Response(gestion_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                
                if organisation_fonctionnement_data:
                    organisation_fonctionnement_data["code_site"] = code_site
                    orga_serializer = FormOrganisationInterneFonctionnementProfilSiteSerializer(data=organisation_fonctionnement_data)
                    if orga_serializer.is_valid():
                        orga_serializer.save()
                        logger.info(f"Saved organisation_fonctionnement for site: {code_site}")
                    else:
                        logger.error(f"Erreur de validation pour organisation_fonctionnement du site '{code_site}': {orga_serializer.errors}")
                        return Response(orga_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                
                if vulnerabilites_data:
                    vulnerabilites_data["code_site"] = code_site
                    vulnerabilites_serializer = FormVulnerabilitePopulationProfilSiteSerializer(data=vulnerabilites_data)
                    if vulnerabilites_serializer.is_valid():
                        vulnerabilites_serializer.save()
                        logger.info(f"Saved vulnerabilites for site: {code_site}")
                    else:
                        logger.error(f"Erreur de validation pour vulnerabilites du site '{code_site}': {vulnerabilites_serializer.errors}")
                        return Response(vulnerabilites_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                
                if abris_ame_data:
                    abris_ame_data["code_site"] = code_site
                    abris_ame_serializer = FormAbrisAmesProfilSiteSerializer(data=abris_ame_data)
                    if abris_ame_serializer.is_valid():
                        abris_ame_serializer.save()
                        logger.info(f"Saved abris_ame for site: {code_site}")
                    else:
                        logger.error(f"Erreur de validation pour abris_ame du site '{code_site}': {abris_ame_serializer.errors}")
                        return Response(abris_ame_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                
                if wash_data:
                    wash_data["code_site"] = code_site
                    wash_serializer = FormWashProfilSiteSerializer(data=wash_data)
                    if wash_serializer.is_valid():
                        wash_serializer.save()
                        logger.info(f"Saved wash for site: {code_site}")
                    else:
                        logger.error(f"Erreur de validation pour wash du site '{code_site}': {wash_serializer.errors}")
                        return Response(wash_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                
                if sante_data:
                    sante_data["code_site"] = code_site
                    sante_serializer = FormSanteProfilSiteSerializer(data=sante_data)
                    if sante_serializer.is_valid():
                        sante_serializer.save()
                        logger.info(f"Saved sante for site: {code_site}")
                    else:
                        logger.error(f"Erreur de validation pour sante du site '{code_site}': {sante_serializer.errors}")
                        return Response(sante_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                
                if securite_alimentaire_data:
                    securite_alimentaire_data["code_site"] = code_site
                    securite_alimentaire_serializer = FormSecuriteAlimentaireProfilSiteSerializer(data=securite_alimentaire_data)
                    if securite_alimentaire_serializer.is_valid():
                        securite_alimentaire_serializer.save()
                        logger.info(f"Saved securite_alimentaire for site: {code_site}")
                    else:
                        logger.error(f"Erreur de validation pour securite_alimentaire du site '{code_site}': {securite_alimentaire_serializer.errors}")
                        return Response(securite_alimentaire_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                
                if protection_data:
                    protection_data["code_site"] = code_site
                    protection_serializer = FormProtectionProfilSiteSerializer(data=protection_data)
                    if protection_serializer.is_valid():
                        protection_serializer.save()
                        logger.info(f"Saved protection for site: {code_site}")
                    else:
                        logger.error(f"Erreur de validation pour protection du site '{code_site}': {protection_serializer.errors}")
                        return Response(protection_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                
                if education_data:
                    education_data["code_site"] = code_site
                    education_serializer = FormEducationProfilSiteSerializer(data=education_data)
                    if education_serializer.is_valid():
                        education_serializer.save()
                        logger.info(f"Saved education for site: {code_site}")
                    else:
                        logger.error(f"Erreur de validation pour education du site '{code_site}': {education_serializer.errors}")
                        return Response(education_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                
                if moyens_subsistance_data:
                    moyens_subsistance_data["code_site"] = code_site
                    moyens_subsistance_serializer = FormMoyenSubsistanceBesoinPrioritaireProfilSiteSerializer(data=moyens_subsistance_data)
                    if moyens_subsistance_serializer.is_valid():
                        moyens_subsistance_serializer.save()
                        logger.info(f"Saved moyens_subsistance for site: {code_site}")
                    else:
                        logger.error(f"Erreur de validation pour moyens_subsistance du site '{code_site}': {moyens_subsistance_serializer.errors}")
                        return Response(moyens_subsistance_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                
                if cartographie_acteurs_services_data:
                    cartographie_acteurs_services_data["code_site"] = code_site
                    cartographie_serializer = FormCartographieServiceActeurProfilSiteSerializer(data=cartographie_acteurs_services_data)
                    if cartographie_serializer.is_valid():
                        cartographie_serializer.save()
                        logger.info(f"Saved cartographie_acteurs_services for site: {code_site}")
                    else:
                        logger.error(f"Erreur de validation pour cartographie_acteurs_services du site '{code_site}': {cartographie_serializer.errors}")
                        return Response(cartographie_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                logger.error(f"Erreur de validation pour le profil du site '{code_site}': {profil_serializer.errors}")
                return Response(profil_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        response = api_response(
            True,
            "Les données ont été chargées avec succès",
        )
        return Response(response, status=status.HTTP_201_CREATED)
    except Exception as e:
        logger.error(f"Error --> {e}")
        response = api_response(
            False, "Un probleme est survenu, veuillez reessayer plus tard"
        )
        return Response(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
@api_view(["GET"])
def get_profil_site_by_code(request, code_site: str):
    try:
        profil = ProfilSite.objects.filter(site__code_site=code_site).order_by("-created_at").first()
        # if not profil:
        #     response = api_response(
        #         False,
        #         f"Aucun profil trouvé pour le site avec le code '{code_site}'.",
        #     )
        #     return Response(response, status=status.HTTP_404_NOT_FOUND)
        
        serializer = ProfilSiteSerializer(profil).data

        site = profil.site if profil else None
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
            obj = model.objects.filter(site=site).order_by("-created_at").first() if site else None
            serializer[key] = serializer_class(obj).data if obj else None
        
        message = f"Profil du site {profil.site.nom_site}" if profil else f"Aucun profil trouvé pour le site avec le code '{code_site}'."
        response = api_response(
            True,
            message,
            serializer,
        )
        return Response(response, status=status.HTTP_200_OK)
    except Exception as e:
        print(f"Error --> {e}")
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
