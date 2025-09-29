# choices.py

OUI_NON_CHOICES = [
    ("Oui", "Oui"),
    ("Non", "Non"),
]
OUI_NON_PARTIELLEMENT_CHOICES = [
    ("Oui", "Oui"),
    ("Partiellement", "Partiellement"),
    ("Non", "Non"),
]
OUI_NON_CHOICES_DATA = [
    "Oui", "Non"
]

SOURCE_EAU_CHOICES = [
    ("Pompe à motricité humaine (PMH)", "Pompe à motricité humaine (PMH)"),
    ("Puits à ciel ouvert", "Puits à ciel ouvert"),
    ("Borne fontaine / Distribution", "Borne fontaine / Distribution"),
    ("Water tracking", "Water tracking"),
    ("Rivière / Cours d'eau", "Rivière / Cours d'eau"),
    ("Vendeur d'eau", "Vendeur d'eau"),
    ("Puits fermé", "Puits fermé"),
    ("Eau en bouteille", "Eau en bouteille"),
    ("Autre", "Autre"),
]
SOURCE_EAU_CHOICES_DATA = [
    "Pompe à motricité humaine (PMH)",
    "Puits à ciel ouvert",
    "Borne fontaine / Distribution",
    "Water tracking",
    "Rivière / Cours d'eau",
    "Vendeur d'eau",
    "Puits fermé",
    "Eau en bouteille",
    "Autre",
]

ELIMINATION_DECHETS_CHOICES = [
    ("Poubelle communale", "Poubelle communale"),
    ("Fosse à ordures", "Fosse à ordures"),
    ("Collecte privée", "Collecte privée"),
    ("Jeter dans la rue / lieu ouvert", "Jeter dans la rue / lieu ouvert"),
    ("Brûlage", "Brûlage"),
    ("Fosse", "Fosse"),
    ("Collecte organisée", "Collecte organisée"),
    ("Autre", "Autre"),
]
ELIMINATION_DECHETS_CHOICES_DATA = [
    "Poubelle communale",
    "Fosse à ordures",
    "Collecte privée",
    "Jeter dans la rue / lieu ouvert",
    "Brûlage",
    "Fosse",
    "Collecte organisée",
    "Autre",
]

TYPE_LATRINE_CHOICES = [
    ("Latrines publiques semi-durables", "Latrines publiques semi-durables"),
    ("Latrines publiques d'urgence", "Latrines publiques d'urgence"),
    ("Latrines privées", "Latrines privées"),
    ("Latrines de fortune (ménages)", "Latrines de fortune (ménages)"),
    ("Pas de latrines", "Pas de latrines"),
]
TYPE_LATRINE_CHOICES_DATA = [
    "Latrines publiques semi-durables",
    "Latrines publiques d'urgence",
    "Latrines privées",
    "Latrines de fortune (ménages)",
    "Pas de latrines",
]

TYPE_DOUCHE_CHOICES = [
    ("Douches publiques (semi-durable)", "Douches publiques (semi-durable)"),
    ("Douches publiques (urgence)", "Douches publiques (urgence)"),
    ("Douches familiales", "Douches familiales"),
    ("Douches de fortune (ménages)", "Douches de fortune (ménages)"),
    ("Pas de douches", "Pas de douches"),
]
TYPE_DOUCHE_CHOICES_DATA = [
    "Douches publiques (semi-durable)",
    "Douches publiques (urgence)",
    "Douches familiales",
    "Douches de fortune (ménages)",
    "Pas de douches",
]

PROBLEMES_SANTE_CHOICES = [
    ("Choléra", "Choléra"),
    ("COVID-19", "COVID-19"),
    ("Handicaps mentaux", "Handicaps mentaux"),
    ("Handicaps physiques", "Handicaps physiques"),
    ("Vers intestinaux", "Vers intestinaux"),
    ("Maladies de la peau", "Maladies de la peau"),
    ("MPOX", "MPOX"),
    ("Séquelles de traumatismes", "Séquelles de traumatismes"),
    ("Nombreux cas de diarrhée", "Nombreux cas de diarrhée"),
    ("Nombreux cas de fièvre", "Nombreux cas de fièvre"),
    ("Maladies respiratoires", "Maladies respiratoires"),
    ("Paludisme", "Paludisme"),
    ("Troubles liés à la grossesse", "Troubles liés à la grossesse"),
    ("Typhoïde", "Typhoïde"),
    ("Autres", "Autres"),
]
PROBLEMES_SANTE_CHOICES_DATA = [
    "Choléra",
    "COVID-19",
    "Handicaps mentaux",
    "Handicaps physiques",
    "Vers intestinaux",
    "Maladies de la peau",
    "MPOX",
    "Séquelles de traumatismes",
    "Nombreux cas de diarrhée",
    "Nombreux cas de fièvre",
    "Maladies respiratoires",
    "Paludisme",
    "Troubles liés à la grossesse",
    "Typhoïde",
    "Autres",
]

DIFFICULTE_SANTE_CHOICES = [
    ("Coût trop élevé", "Coût trop élevé"),
    ("Pas de personnel qualifié", "Pas de personnel qualifié"),
    ("Pas d'argent pour traitement", "Pas d'argent pour traitement"),
    ("Établissement mal équipé", "Établissement mal équipé"),
    ("Établissement trop éloigné", "Établissement trop éloigné"),
    ("Pas de transport", "Pas de transport"),
    ("Médicaments non disponibles", "Médicaments non disponibles"),
    ("Barriere de la langue", "Barrière de la langue"),
    ("Refus du traitement", "Refus du traitement"),
    ("Établissement fermé", "Établissement fermé"),
    ("Aucun", "Aucun"),
    ("Autres", "Autres"),
]
DIFFICULTE_SANTE_CHOICES_DATA = [
    "Coût trop élevé",
    "Pas de personnel qualifié",
    "Pas d'argent pour traitement",
    "Établissement mal équipé",
    "Établissement trop éloigné",
    "Pas de transport",
    "Médicaments non disponibles",
    "Barrière de la langue",
    "Refus du traitement",
    "Établissement fermé",
    "Aucun",
    "Autres",
]

COMITES_GESTION_CHOICES = [
    ("Comité de gestion du SITE", "Comité de gestion du SITE"),
    ("Comité des femmes", "Comité des femmes"),
    ("Comité des jeunes", "Comité des jeunes"),
    ("Comité éducation", "Comité éducation"),
    ("Comité santé", "Comité santé"),
    ("Comité de distribution", "Comité de distribution"),
    ("Comité de maintenance", "Comité de maintenance"),
    ("Comité WASH", "Comité WASH"),
    ("Autre comité", "Autre comité"),
]
COMITES_GESTION_CHOICES_DATA = [
    "Comité de gestion du SITE",
    "Comité des femmes",
    "Comité des jeunes",
    "Comité éducation",
    "Comité santé",
    "Comité de distribution",
    "Comité de maintenance",
    "Comité WASH",
    "Autre comité",
]

COMITES_FONCTIONNELS_CHOICES = [
    ("Tous les comités fonctionnent", "Tous les comités fonctionnent"),
    ("Partiellement", "Partiellement"),
    ("Aucun", "Aucun"),
]

RENCONTRES_PLANIFICATION_CHOICES = [
    ("Hebdommadaire", "Hebdommadaire"),
    ("Bi-hebdomadaire", "Bi-hebdomadaire"),
    ("Mensuelle (1 fois chaque mois)", "Mensuelle (1 fois chaque mois)"),
]

# OPTIONS CHOICES

TYPE_SITE_OPTIONS = [
    "Site Planifié",
    "Site Spontané",
    "Centre Collectif",
    "Autre",
]

TYPE_PROPRIETE_FONCIERE_OPTIONS = [
    "Gouvernement",
    "Mairie",
    "Privée",
    "Autre",
]

TYPE_INSTALLATION_OPTIONS = [
    "Urbain",
    "Peri-urbain",
    "Rural",
]

STATUT_SITE_OPTIONS = [
    "Fonctionnel",
    "Fermé",
]

OUI_NON_OPTIONS = [
    "Oui",
    "Non",
]

SEXE_OPTIONS = [
    "Masculin",
    "Féminin",
]

COMITES_OPTIONS = [
    "Comité de gestion du SITE",
    "Comité des femmes",
    "Comité des jeunes",
    "Comité éducation",
    "Comité santé",
    "Comité de distribution",
    "Comité de maintenance",
    "Comité WASH",
    "Autre comité",
]

ETAT_COMITES_OPTIONS = [
    "Tous les comités fonctionnent",
    "Partiellement",
    "Aucun",
]

OUI_PARTIELLEMENT_NON_OPTIONS = [
    "Oui",
    "Partiellement",
    "Non",
]

MOYENS_COMMINICATION_DISTRIBUTION_OPTIONS = [
    "Équipe de gestion du site",
    "ONG",
    "Télévision",
    "Matériel imprimé (bannières/posters/pamphlets)",
    "Facebook",
    "Bouche à oreille",
    "Internet (sites d'information)",
    "Autorités locales",
    "Dirigeants communautaires",
    "Radio",
    "Journaux",
    "Téléphones portables",
    "Haut-parleurs",
    "Comités de site",
    "Autre",
]

RAISONS_RETOURS_OPTIONS = [
    "Pas d’opportunités d’emploi en ce lieu (localité où il y a le site)",
    "Pas d’opportunités pour l’éducation des enfants",
    "Difficulté d’accès aux services sanitaires",
    "Absence d’assistance humanitaire ici (sur le site uniquement).",
    "Rejoindre des membres de famille",
    "Détérioration de la situation sécuritaire (site, village ou commune d’accueil)",
    "Autres",
]

TYPE_ABRIS_OPTIONS = [
    "Tente en bache",
    "Tente en materiaux",
    "Tente en planche",
    "Tente en feuille",
    "Tente en tissus",
    "Autre",
]

AME_BASE_CHOICES = [
    "Articles de literie (draps de lit, oreillers)",
    "Matelas/tapis de couchage",
    "Couvertures",
    "Natte",
    "Ustensiles de cuisine",
    "Kit d’hygiène intime",
    "Bidon/Stockage de l'eau",
    "Moustiquaire",
    "Bassine de lavage",
    "Foyer amélioré/Réchaud de cuisine",
    "Savon de lessive",
    "Bâche",
    "Combustible de cuisine",
    "Stockage de l'eau",
    "Vêtements",
    "Lampe solaire",
    "Combustible de chauffage (Ex: bois de chauffauge, pétrole etc.)",
    "Stockage du combustible",
    "Aucun des éléments ci-dessus",
    "Autre",
]

AME_SAISON_SECHE_CHOICES = [
    "Stockage d'eau supplémentaire",
    "Vêtements adaptés à la chaleur",
    "Aucun des éléments ci-dessus",
    "Autre",
]

STATEGIES_COURANTES_MANQUE_AME_OPTIONS = [
    "Pas besoin d'utiliser une stratégie d'adaptation car il n'y a pas de problème d'abri ou de AME",
    "Vente d'actifs/de biens du ménage (bijoux, téléphone, etc.)",
    "Vente/location d'une parcelle d'abri",
    "Vente de certains articles d'assistance reçus",
    "Réduction de la consommation alimentaire",
    "Dépenser ses économies",
    "Emprunter de l'argent / acheter à crédit",
    "Travail à haut risque / illégal",
    "Envoyer les enfants au travail",
    "Créer de petits magasins/entreprises dans le SITE",
    "Autre",
]

ETAT_GENERAL_PARCELLES_ROUTES_CANIVEAUX_OPTIONS = [
    "Bon",
    "Besoin d'un entretien léger",
    "Besoin d'un entretien lourd",
    "Nécessite une amélioration",
    "Pas de caniveaux",
]

SOURCES_PRINCIPALES_ELECTRICITE_OPTIONS = [
    "Réseau électrique",
    "Générateurs centralisés",
    "Générateurs privés",
    "Poteaux solaires",
    "Aucune source d'électricité",
]

SOURCE_PRINCIPALE_EAU_POTABLE_OPTIONS = [
    "ONEA (accès communal)",
    "Pompe à motricité humaine (PMH)",
    "Puit à ciel ouvert",
    "Puit fermé",
    "Distribution d’eau/Borne fontaine",
    "Rivière/cours d’eau/étendue d’eau",
    "Vendeur d'eau",
    "Achetée au magasin (Eau en bouteille)",
    "Water tracking",
    "Autre",
]

METHODES_ELIMINATION_DECHET_OPTIONS = [
    "Collecte municipale",
    "Collecte privée",
    "Poubelle communale",
    "Fosse à ordures",
    "Brûler",
    "Jeter dans la rue / lieu ouvert",
]

TYPES_LATRINES_DOUCHES_OPTIONS = [
    "Latrines publiques semi-durables",
    "Latrines publiques d'urgence",
    "Latrines privées",
    "Latrines de fortune ménages",
    "Pas de latrines",
    
    "Douches publiques semi-durable",
    "Douches publiques urgence",
    "Douches familiales",
    "Douches privées",
    "Douches de fortune ménages",
    "Pas de douches",
]

PROBLEMES_SANTE_RESIDENTS_OPTIONS = [
    "Nombreux cas de diarrhée",
    "Maladies de la peau (gale, éruptions contagieuses, etc.)",
    "Nombreux cas de fièvre",
    "Nombreux cas de paludisme",
    "Nombreux cas de maladies respiratoires",
    "Nombreux cas de troubles liées à la grossesse",
    "Nombreuses séquelles de traumatismes",
    "Handicaps physiques",
    "Handicaps mentaux",
    "Choléra",
    "Autres",
    "Typhoïde",
    "Hépatite A/E",
    "Helminthes transmis par le sol (vers intestinaux)",
    "COVID-19",
    "Aucun",
    "Autres problèmes de santé",
]

PROBLEMES_FAMILLES_ACCES_SOINS_OPTIONS = [
    "Le coût des soins de santé était trop élevé",
    "Pas de professionnels de santé qualifiés",
    "L'établissement n'était pas équipé pour faire face au problème",
    "Les établissements étaient trop éloignés",
    "Fonds insuffisants pour acheter le traitement/les médicaments",
    "Médicaments non disponibles",
    "Refus du traitement",
    "Barrière de la langue",
    "Manque de documents civils corrects",
    "Installations non ouvertes",
    "Pas de transport disponible",
    "Coût du transport trop élevé",
    "Autres",
    "Aucun",
]

# NOMBRE_REPAS_PAR_JOUR_OPTIONS = [
#     "Un repas",
#     "Trois repas",
#     "Deux repas",
#     "Pas de repas",
# ]

DIFFICULTES_ACCES_NOURRITURE = [
    "Pas d'installations de cuisson",
    "Accès limité à la nourriture en raison de contraintes physiques/logistiques (par exemple, routes endommagées, absence de véhicules, longue distance).",
    "Accès limité à la nourriture en raison de contraintes de sécurité",
    "Accès limité à la nourriture en raison de ressources économiques limitées",
    "La production agricole/élevage est perturbée",
    "Les aliments disponibles sont de mauvaise qualité",
    "Aucune",
    "Autres",
]

FREQUENCE_AIDES_ALIMENTAIRE_OPTIONS = [
    "Tous les jours",
    "Chaque semaine",
    "Tous les mois",
    "Entre 2 et 3 mois",
    "Jamais",
]

RESTRICTIONS_MOUVEMENT_OPTIONS = [
    "Nécessité d'obtenir des autorisations/coupons de sécurité",
    "Obligation de présenter des documents d'identité aux autorités civiles ou aux acteurs de la sécurité pour sortir/entrer dans le site.",
    "Restrictions temporelles concernant les dates de départ et de retour",
    "Nécessité de fournir une raison spécifique pour le mouvement (emploi, médical, scolaire)",
    "Barrages routiers physiques",
    "Autres",
]

OUI_NON_JE_PREFERE_NON_REPONDRE = [
    "Oui",
    "Non",
    "Je ne sais pas",
    "Je préfère ne pas répondre",
]

ACTEURS_INCIDENTS_IMPLIQUES_OPTIONS = [
    "Communauté d'accueil",
    "FDS (Militaire, gendamerie)",
    "Police",
    "Autorités locales",
    "Groupes armés non identifiés",
    "Résidents du site",
    "Préfère ne pas répondre",
    "Autres",
]

MENANCES_COURANTES_OPTIONS = [
    "Conditions de travail illégales, dangereuses ou exploitantes",
    "Crainte des acteurs armés de la sécurité (recrutement, détention, violence, menaces ou harcèlement)",
    "Crainte des groupes communautaires/tribaux (violence, menaces, harcèlement liés à un conflit en cours).",
    "Crainte des groupes d'opposition armés (recrutement, violence, menaces ou harcèlement)",
    "Expulsion",
    "Friction entre les communautés",
    "Incendie",
    "Inondations",
    "Maladies infectieuses",
    "Proximité d'un conflit (attaques armées, ligne de front, etc.)",
    "Risque d'explosion (mines, bombes, engins explosifs improvisés)",
    "VBG à l'intérieur et à l'extérieur du foyer",
    "Autre",
]

ZONES_INSECURES_OPTIONS = [
    "Centre de distribution",
    "Dans les abris",
    "École",
    "Établissement de santé",
    "Installations WASH (latrines/bains)",
    "Marché",
    "Point d'eau",
    "Préfère ne pas dire",
    "Aucun",
    "Autres",
]

TYPES_SERVICES_SOUTIEN_PSYCHOSOCIAL_OPTIONS = [
    "Conseil de groupe",
    "Conseil individuel",
    "Espace adapté aux enfants/activités récréatives PSS",
    "Groupes PSS structurés (par ex. groupes de pairs)",
    "Premiers secours psychologiques",
    "PSS par la gestion de cas",
    "Autres",
]

PRINCIPALES_OBSTACLES_ACCES_EDUCTIONS = [
    "Pas assez d'écoles ou de salles de classe",
    "Pas assez d'enseignants",
    "Pas assez de matériel pédagogique",
    "Contraintes physiques/logistiques",
    "Longue distance à parcourir pour se rendre à l'école",
    "Ressources économiques limitées (par exemple, pour payer les frais de scolarité, l'uniforme, le transport, les livres, etc.)",
    "Contraintes de sécurité (par exemple, présence de munitions non explosées dans ou autour de l'école)",
    "L'école est utilisée à d'autres fins, par exemple comme abri.",
    "École fermée",
    "Autre",
    "Aucun",
]

ARTICLES_BESOIN_EXISTANT_MARCHE_OPTIONS = [
    "Produits alimentaires de base",
    "Eau",
    "Articles ménagers de base (par exemple, matelas, couvertures, ustensiles de cuisine)",
    "Outils, matériel et matériaux",
    "Articles d'hygiène",
    "Médicaments de base",
    "Carburant",
    "Autres",
    "Tout ce qui est nécessaire est disponible",
]

PRINCIPAUX_MOYENS_SUBSISTANCE_OPTIONS = [
    "Agriculture commerciale",
    "L'agriculture des petits exploitants",
    "Agriculture de subsistance",
    "Travail agricole non qualifié",
    "Main-d'œuvre salariée non qualifiée",
    "Travail occasionnel non qualifié",
    "Travail indépendant",
    "Industrie des services peu qualifiés",
    "Secteur public/fonctionnaire",
    "Agent de la sécurité publique",
    "Industrie des services qualifiés",
    "Pension de l'État",
    "Sécurité sociale",
    "Cadeaux (en nature ou en espèces de la part d'amis ou de parents)",
    "Prêts",
    "Aide humanitaire",
    "Épargne",
    "Vente de biens",
    "Autres",
]

BESOINS_PRIORITAIRES_OPTIONS = [
    "Abris/Assistance en maintenance abri",
    "Amenagement du site",
    "Assistance en moyens d'existence (AGR)",
    "Assistance medicale",
    "Assistance psycho-sociale",
    "Eau potable",
    "Education",
    "Eclairage du site",
    "Élimination des déchets",
    "Enregistrement",
    "Espace amis des enfants/activités récréatives",
    "Latrine/Douche",
    "NFI",
    "Nutrition",
    "Service de nutrition",
    "Service de protection",
    "Service de protection",
    "Service juridique",
    "Service sanitaire",
    "Soins de santé",
    "Vivres",
]

ETAT_SERVICES_OPTIONS = [
    "Adequat",
    "Inadequat",
    "Inexistant",
]