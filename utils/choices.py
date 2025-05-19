# choices.py

OUI_NON_CHOICES = [
    ("Oui", "Oui"),
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