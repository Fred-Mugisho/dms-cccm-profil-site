from django.contrib import admin
# from .models import *
from django.contrib.auth.models import Group

from .customs_models.bases.profil_site import ProfilSite

from .customs_models.autres.gestion_admin_site import GestionAdminProfilSite
from .customs_models.autres.gouvernance_participation_site import OrganisationInterneFonctionnementProfilSite
from .customs_models.autres.moyens_subsistance_besoins_prioritaires import MoyenSubsistanceBesoinPrioritaireProfilSite
from .customs_models.autres.vulnerabilite_site import VulnerabilitePopulationProfilSite

from .customs_models.secteurs.abris_ames_site import AbrisAmesProfilSite, DetailsTypeAbrisProfilSite
from .customs_models.secteurs.cartographie_service_acteurs import CartographieServiceActeurProfilSite
from .customs_models.secteurs.eduction import EducationProfilSite
from .customs_models.secteurs.protection import ProtectionProfilSite
from .customs_models.secteurs.sante_site import SanteProfilSite
from .customs_models.secteurs.securite_alimentaire import SecuriteAlimentaireProfilSite
from .customs_models.secteurs.wash_site import WashProfilSite


admin.site.unregister(Group)

models_list = [
    # InformationGeneraleProfilSite,
    # GestionSite,
    # WashSite,
    # SanteSite,
    
    ProfilSite, 

    GestionAdminProfilSite,
    OrganisationInterneFonctionnementProfilSite,
    MoyenSubsistanceBesoinPrioritaireProfilSite,
    VulnerabilitePopulationProfilSite,

    AbrisAmesProfilSite,
    DetailsTypeAbrisProfilSite,
    CartographieServiceActeurProfilSite,
    EducationProfilSite,
    ProtectionProfilSite,
    SanteProfilSite,
    SecuriteAlimentaireProfilSite,
    WashProfilSite
]
admin.site.register(models_list)