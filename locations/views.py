from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import *
from .serializers import *
from django.http import HttpResponse
import openpyxl
from openpyxl.utils import get_column_letter
from openpyxl.styles import Font
from collections import defaultdict
from utils.functions import *

@api_view(['GET'])
def locations(request):
    try:
        provinces = Province.objects.all().order_by('name')
        serializer = ProvinceSerializer(provinces, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
@api_view(['POST', 'PUT'])
def load_locations_from_excel(request):
    try:
        locations_data = request.FILES.get('locations')
        if not locations_data:
            return Response({"message": "Fichier des localisations manquant"}, status=status.HTTP_400_BAD_REQUEST)

        wb = openpyxl.load_workbook(locations_data)
        sheets_name = ["Provinces", "Territoires", "Secteurs", "Groupements", "Villages", "Zones de sante", "Aires de sante"]
        
        for sheet_name in sheets_name:
            if sheet_name not in wb.sheetnames:
                continue  # Ignore les feuilles non présentes
            
            sheet = wb[sheet_name]
            for row in sheet.iter_rows(min_row=2, values_only=True):
                if not row or not row[0]:  # Ignore les lignes vides
                    continue
                
                if sheet_name == "Provinces":
                    Province.objects.update_or_create(
                        code=row[0], 
                        defaults={'name': row[1]}
                    )

                elif sheet_name == "Territoires":
                    province = Province.objects.filter(code=row[2]).first()
                    if not province:
                        continue  # Ou collecter les erreurs
                    Territoire.objects.update_or_create(
                        code=row[0], 
                        defaults={'name': row[1], 'province': province}
                    )
                    
                elif sheet_name == "Secteurs":
                    territoire = Territoire.objects.filter(code=row[2]).first()
                    if not territoire:
                        continue
                    Secteur.objects.update_or_create(
                        code=row[0], 
                        defaults={'name': row[1], 'territoire': territoire}
                    )

                elif sheet_name == "Groupements":
                    secteur = Secteur.objects.filter(code=row[2]).first()
                    if not secteur:
                        continue
                    Groupement.objects.update_or_create(
                        code=row[0], 
                        defaults={'name': row[1], 'secteur': secteur}
                    )

                elif sheet_name == "Villages":
                    groupement = Groupement.objects.filter(code=row[2]).first()
                    if not groupement:
                        continue
                    Village.objects.update_or_create(
                        code=row[0], 
                        defaults={'name': row[1], 'groupement': groupement, 'latitude': row[3], 'longitude': row[4]}
                    )

                elif sheet_name == "Zones de sante":
                    territoire = Territoire.objects.filter(code=row[2]).first()
                    if not territoire:
                        continue
                    ZoneSante.objects.update_or_create(
                        code=row[0], 
                        defaults={'name': row[1], 'territoire': territoire, 'latitude': row[3], 'longitude': row[4]}
                    )
                    
                elif sheet_name == "Aires de sante":
                    health_zone = ZoneSante.objects.filter(code=row[2]).first()
                    if not health_zone:
                        continue
                    AireSante.objects.update_or_create(
                        code=row[0], 
                        defaults={'name': row[1], 'health_zone': health_zone, 'latitude': row[3], 'longitude': row[4]}
                    )

        return Response({"message": "Les données des localisations ont été chargées avec succès"}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"message": f"Erreur : {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
@api_view(['GET'])
def get_province(request, id):
    try:
        province = Province.objects.get(id=id)
        serializer = ProvinceSerializer(province)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Province.DoesNotExist:
        return Response({"message": "Province n'existe pas"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
@api_view(['POST', 'PUT'])
def create_update_province(request, id=None):
    try:
        province = Province.objects.get(id=id) if id else None
        province_form = ProvinceFormSerializer(province, data=request.data)
        if province_form.is_valid():
            province_form.save()
            return Response(province_form.data, status=status.HTTP_200_OK)
        else:
            return Response(province_form.errors, status=status.HTTP_400_BAD_REQUEST)
    except Province.DoesNotExist:
        return Response({"message": "Province n'existe pas"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
@api_view(['GET'])
def get_territoire(request, id):
    try:
        territoire = Territoire.objects.get(id=id)
        serializer = TerritoireSerializer(territoire)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Territoire.DoesNotExist:
        return Response({"message": "Territoire n'existe pas"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
@api_view(['POST', 'PUT'])
def create_update_territoire(request, id=None):
    try:
        territoire = Territoire.objects.get(id=id) if id else None
        territoire_form = TerritoireFormSerializer(territoire, data=request.data)
        if territoire_form.is_valid():
            territoire_form.save()
            return Response(territoire_form.data, status=status.HTTP_200_OK)
        else:
            return Response(territoire_form.errors, status=status.HTTP_400_BAD_REQUEST)
    except Territoire.DoesNotExist:
        return Response({"message": "Territoire n'existe pas"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
@api_view(['GET'])
def get_secteur(request, id):
    try:
        secteur = Secteur.objects.get(id=id)
        serializer = SecteurSerializer(secteur)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Secteur.DoesNotExist:
        return Response({"message": "Secteur n'existe pas"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
@api_view(['POST', 'PUT'])
def create_update_secteur(request, id=None):
    try:
        secteur = Secteur.objects.get(id=id) if id else None
        secteur_form = SecteurFormSerializer(secteur, data=request.data)
        if secteur_form.is_valid():
            secteur_form.save()
            return Response(secteur_form.data, status=status.HTTP_200_OK)
        else:
            return Response(secteur_form.errors, status=status.HTTP_400_BAD_REQUEST)
    except Secteur.DoesNotExist:
        return Response({"message": "Secteur n'existe pas"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
@api_view(['GET'])
def get_groupement(request, id):
    try:
        groupement = Groupement.objects.get(id=id)
        serializer = GroupementSerializer(groupement)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Groupement.DoesNotExist:
        return Response({"message": "Groupement n'existe pas"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
@api_view(['POST', 'PUT'])
def create_update_groupement(request, id=None):
    try:
        groupement = Groupement.objects.get(id=id) if id else None
        groupement_form = GroupementFormSerializer(groupement, data=request.data)
        if groupement_form.is_valid():
            groupement_form.save()
            return Response(groupement_form.data, status=status.HTTP_200_OK)
        else:
            return Response(groupement_form.errors, status=status.HTTP_400_BAD_REQUEST)
    except Groupement.DoesNotExist:
        return Response({"message": "Groupement n'existe pas"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
@api_view(['GET'])
def get_village(request, id):
    try:
        village = Village.objects.get(id=id)
        serializer = VillageSerializer(village)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Village.DoesNotExist:
        return Response({"message": "Village n'existe pas"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
@api_view(['POST', 'PUT'])
def create_update_village(request, id=None):
    try:
        village = Village.objects.get(id=id) if id else None
        village_form = VillageFormSerializer(village, data=request.data)
        if village_form.is_valid():
            village_form.save()
            return Response(village_form.data, status=status.HTTP_200_OK)
        else:
            return Response(village_form.errors, status=status.HTTP_400_BAD_REQUEST)
    except Village.DoesNotExist:
        return Response({"message": "Village n'existe pas"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
@api_view(['GET'])
def get_zone_sante(request, id):
    try:
        zone_sante = ZoneSante.objects.get(id=id)
        serializer = ZoneSanteSerializer(zone_sante)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except ZoneSante.DoesNotExist:
        return Response({"message": "Zone sante n'existe pas"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
@api_view(['POST', 'PUT'])
def create_update_zone_sante(request, id=None):
    try:
        zone_sante = ZoneSante.objects.get(id=id) if id else None
        zone_sante_form = ZoneSanteFormSerializer(zone_sante, data=request.data)
        if zone_sante_form.is_valid():
            zone_sante_form.save()
            return Response(zone_sante_form.data, status=status.HTTP_200_OK)
        else:
            return Response(zone_sante_form.errors, status=status.HTTP_400_BAD_REQUEST)
    except ZoneSante.DoesNotExist:
        return Response({"message": "Zone sante n'existe pas"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
@api_view(['GET'])
def get_aire_sante(request, id):
    try:
        aire_sante = AireSante.objects.get(id=id)
        serializer = AireSanteSerializer(aire_sante)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except AireSante.DoesNotExist:
        return Response({"message": "Aire sante n'existe pas"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
@api_view(['POST', 'PUT'])
def create_update_aire_sante(request, id=None):
    try:
        aire_sante = AireSante.objects.get(id=id) if id else None
        aire_sante_form = AireSanteFormSerializer(aire_sante, data=request.data)
        if aire_sante_form.is_valid():
            aire_sante_form.save()
            return Response(aire_sante_form.data, status=status.HTTP_200_OK)
        else:
            return Response(aire_sante_form.errors, status=status.HTTP_400_BAD_REQUEST)
    except AireSante.DoesNotExist:
        return Response({"message": "Aire sante n'existe pas"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class DemographicDataExtractor:
    """Classe pour extraire et calculer les données démographiques"""
    
    # Coefficients pour la répartition des tranches d'âge
    AGE_DISTRIBUTION = {
        '0_5_to_0_4': 0.8,
        '0_5_to_5_11': 0.2,
        '6_17_to_5_11': 0.5,
        '6_17_to_12_17': 0.5,
        '18_59_to_18_24': 0.4,
        '18_59_to_25_59': 0.6
    }
    
    @classmethod
    def extract_demographic_data(cls, row):
        """Extrait et calcule les données démographiques détaillées"""
        try:
            # Données brutes par genre et tranche d'âge
            raw_data = {
                'individus_0_5_f': safe_int(row[14]),
                'individus_6_17_f': safe_int(row[15]),
                'individus_18_59_f': safe_int(row[16]),
                'individus_60_f': safe_int(row[17]),
                'individus_0_5_h': safe_int(row[18]),
                'individus_6_17_h': safe_int(row[19]),
                'individus_18_59_h': safe_int(row[20]),
                'individus_60_h': safe_int(row[21])
            }
            
            # Calcul des tranches d'âge détaillées
            detailed_data = {}
            
            # Pour les femmes
            detailed_data['individus_0_4_f'] = int(raw_data['individus_0_5_f'] * cls.AGE_DISTRIBUTION['0_5_to_0_4'])
            detailed_data['individus_5_11_f'] = int(
                raw_data['individus_0_5_f'] * cls.AGE_DISTRIBUTION['0_5_to_5_11'] + 
                raw_data['individus_6_17_f'] * cls.AGE_DISTRIBUTION['6_17_to_5_11']
            )
            detailed_data['individus_12_17_f'] = int(raw_data['individus_6_17_f'] * cls.AGE_DISTRIBUTION['6_17_to_12_17'])
            detailed_data['individus_18_24_f'] = int(raw_data['individus_18_59_f'] * cls.AGE_DISTRIBUTION['18_59_to_18_24'])
            detailed_data['individus_25_59_f'] = int(raw_data['individus_18_59_f'] * cls.AGE_DISTRIBUTION['18_59_to_25_59'])
            detailed_data['individus_60_f'] = raw_data['individus_60_f']
            
            # Pour les hommes
            detailed_data['individus_0_4_h'] = int(raw_data['individus_0_5_h'] * cls.AGE_DISTRIBUTION['0_5_to_0_4'])
            detailed_data['individus_5_11_h'] = int(
                raw_data['individus_0_5_h'] * cls.AGE_DISTRIBUTION['0_5_to_5_11'] + 
                raw_data['individus_6_17_h'] * cls.AGE_DISTRIBUTION['6_17_to_5_11']
            )
            detailed_data['individus_12_17_h'] = int(raw_data['individus_6_17_h'] * cls.AGE_DISTRIBUTION['6_17_to_12_17'])
            detailed_data['individus_18_24_h'] = int(raw_data['individus_18_59_h'] * cls.AGE_DISTRIBUTION['18_59_to_18_24'])
            detailed_data['individus_25_59_h'] = int(raw_data['individus_18_59_h'] * cls.AGE_DISTRIBUTION['18_59_to_25_59'])
            detailed_data['individus_60_h'] = raw_data['individus_60_h']
            
            return detailed_data
            
        except Exception as e:
            logging.error(f"Erreur lors de l'extraction des données démographiques: {e}")
            # Retourner des valeurs par défaut en cas d'erreur
            return {field: 0 for field in [
                'individus_0_4_f', 'individus_5_11_f', 'individus_12_17_f',
                'individus_18_24_f', 'individus_25_59_f', 'individus_60_f',
                'individus_0_4_h', 'individus_5_11_h', 'individus_12_17_h',
                'individus_18_24_h', 'individus_25_59_h', 'individus_60_h'
            ]}
            
class LocationDataExtractor:
    """Classe pour extraire et calculer les données démographiques"""
    
    @classmethod
    def extract_location_data(cls, row):
        """Extrait et calcule les données démographiques détaillées"""
        try:
            # Données brutes par genre et tranche d'âge
            location_data = {
                'province': safe_str(row[1]),
                'code_province': safe_str(row[2]),
                'territoire': safe_str(row[3]),
                'code_territoire': safe_str(row[4]),
                'zone_sante': safe_str(row[5]),
                'code_zone_sante': safe_str(row[6]),
                'type_site': safe_str(row[9]),
                'longitude': safe_str(row[10]),
                'latitude': safe_str(row[11]),
            }
            return location_data
        except Exception as e:
            logging.error(f"Erreur lors de l'extraction des données démographiques: {e}")
            # Retourner des valeurs par défaut en cas d'erreur
            return {field: "" for field in [
                'province', 'code_province', 'territoire', 'code_territoire', 'zone_sante', 'code_zone_sante', 'type_site', 'longitude', 'latitude'
            ]}

class MovementCalculator:
    """Classe pour calculer les mouvements entre périodes"""
    
    DEMOGRAPHIC_FIELDS = [
        'individus_0_4_f', 'individus_5_11_f', 'individus_12_17_f',
        'individus_18_24_f', 'individus_25_59_f', 'individus_60_f',
        'individus_0_4_h', 'individus_5_11_h', 'individus_12_17_h',
        'individus_18_24_h', 'individus_25_59_h', 'individus_60_h'
    ]
    
    @classmethod
    def calculate_movements(cls, previous_data, current_data):
        """Calcule les mouvements entre deux périodes"""
        movements = []
        
        try:
            # Calcul des deltas principaux
            delta_menages = current_data['menages'] - previous_data['menages']
            delta_individus = current_data['individus'] - previous_data['individus']
            
            # Si pas de changement, pas de mouvement
            if delta_individus == 0 and delta_menages == 0:
                return movements
            
            # Calcul des deltas démographiques détaillés
            demographic_deltas = {}
            for field in cls.DEMOGRAPHIC_FIELDS:
                demographic_deltas[f'delta_{field}'] = (
                    current_data.get(field, 0) - previous_data.get(field, 0)
                )
            
            # Détermination du type de mouvement
            movement_type = "entree" if delta_individus >= 0 else "sortie"
            
            movement = {
                'type_mouvement': movement_type,
                'delta_menages': delta_menages,
                'delta_individus': delta_individus,
                **demographic_deltas
            }
            
            movements.append(movement)
            return movements
            
        except Exception as e:
            logging.error(f"Erreur lors du calcul des mouvements: {e}")
            return []

class SiteDataProcessor:
    """Classe pour traiter les données par site"""
    
    @classmethod
    def create_new_record(cls, data):
        """Crée un nouvel enregistrement basé sur les données existantes"""
        try:
            code_site = data['code_site']
            nom_site = data['nom_site']

            # Récupération des données existantes pour ce site
            existing_data = DataImport.objects.filter(nom_site=nom_site).order_by('date_mise_a_jour')

            # Données de la mise à jour actuelle
            current_data = {
                'menages': data['menages'],
                'individus': data['individus'],
                'date_mise_a_jour': data['date_mise_a_jour']
            }

            # Champs démographiques
            demographic_fields = MovementCalculator.DEMOGRAPHIC_FIELDS
            
            # Calcul des totaux actuels
            totals = {'menages': 0, 'individus': 0}
            for field in demographic_fields:
                totals[field] = 0

            # Agrégation des données existantes
            for record in existing_data:
                factor = 1 if record.type_mouvement in ["donnee_brute", "entree"] else -1
                totals['menages'] += factor * record.menages
                totals['individus'] += factor * record.individus
                
                for field in demographic_fields:
                    totals[field] += factor * getattr(record, field, 0)

            # Détermination du type de mouvement
            delta_menages = current_data['menages'] - totals['menages']
            delta_individus = current_data['individus'] - totals['individus']
            movement_type = 'entree' if current_data['individus'] >= totals['individus'] else 'sortie'
            
            logging.info(f"Site : {nom_site} - {current_data['date_mise_a_jour']}")
            # logging.info(f"Menages : {current_data['menages']} - {totals['menages']} = {delta_menages}")
            logging.info(f"Individus : {current_data['individus']} - {totals['individus']} = {delta_individus}")
            logging.info(f"Type de mouvement : {movement_type}")
            logging.info("-" * 20)
            

            if delta_individus != 0:
                # Construction du nouveau record
                new_record = {
                    'code_site': code_site,
                    'nom_site': nom_site,
                    'menages': abs(delta_menages),
                    'individus': abs(delta_individus),
                    'date_mise_a_jour': current_data['date_mise_a_jour'],
                    'type_mouvement': movement_type,
                }
                
                for field_loc in ['province', 'code_province', 'territoire', 'code_territoire', 'zone_sante', 'code_zone_sante', 'type_site', 'longitude', 'latitude']:
                    new_record[field_loc] = data.get(field_loc, '')

                # Ajout des données démographiques
                for field in demographic_fields:
                    if delta_individus != 0:
                        new_record[field] = abs(data.get(field, 0) - totals[field])

                return new_record
            else:
                return None
        except Exception as e:
            logging.error(f"Erreur lors de la création du nouvel enregistrement: {e}")
            raise

class DataImportService:
    """Service principal pour l'importation des données"""
    
    # Configuration des feuilles par ordre chronologique
    SHEETS_CONFIG = [
        ('Mai2023', '2023-05-31'),
        ('Juin2023', '2023-06-30'),
        ('Juillet2023', '2023-07-31'),
        ('Aout2023', '2023-08-31'),
        ('Sept2023', '2023-09-30'),
        ('Oct2023', '2023-10-31'),
        ('Nov2023', '2023-11-30'),
        ('Dec2023', '2023-12-31'),
        ('Jan2024', '2024-01-31'),
        ('Fev2024', '2024-02-28'),
        ('Mars2024', '2024-03-31'),
        ('Avril2024', '2024-04-30'),
        ('Mai2024', '2024-05-31'),
        ('Juin2024', '2024-06-30'),
        ('Juillet2024', '2024-07-31'),
        ('Aout2024', '2024-08-31'),
        ('Sept2024', '2024-09-30'),
        ('Oct2024', '2024-10-31'),
        ('Nov2024', '2024-11-30'),
        ('Jan2025', '2025-01-31'),
        ('Fev2025', '2025-02-28'),
        ('Mars2025', '2025-03-31'),
    ]
    
    def __init__(self):
        self.extractor = DemographicDataExtractor()
        self.location = LocationDataExtractor()
        self.calculator = MovementCalculator()
        self.processor = SiteDataProcessor()
    
    def process_sheet_data(self, sheet, sheet_name, default_date):
        """Traite les données d'une feuille Excel"""
        processed_data = []
        row_count = 0
        
        try:
            for row in sheet.iter_rows(min_row=2, values_only=True):
                if not row or not row[0]:
                    continue
                
                row_count += 1
                
                # Extraction des données démographiques
                demo_data = self.extractor.extract_demographic_data(row)
                location_data = self.location.extract_location_data(row)
                
                # Gestion de la date
                date_mise_a_jour = default_date
                
                # Construction de l'entrée de données
                data_entry = {
                    **location_data,
                    'nom_site': safe_str(row[7]),
                    'code_site': safe_str(row[8]),
                    'menages': safe_int(row[12]),
                    'individus': safe_int(row[13]),
                    'date_mise_a_jour': date_mise_a_jour,
                    **demo_data
                }
                
                processed_data.append(data_entry)
                
        except Exception as e:
            logging.error(f"Erreur lors du traitement de la feuille {sheet_name}: {e}")
            raise
        
        return processed_data, row_count
    
    def create_record_dict(self, data, movement_type):
        """Crée un dictionnaire d'enregistrement"""
        record = {
            'code_site': data['code_site'],
            'nom_site': data['nom_site'],
            'menages': data['menages'],
            'individus': data['individus'],
            'date_mise_a_jour': data['date_mise_a_jour'],
            'type_mouvement': movement_type,
        }
        for field_loc in ['province', 'code_province', 'territoire', 'code_territoire', 'zone_sante', 'code_zone_sante', 'type_site', 'longitude', 'latitude']:
            record[field_loc] = data.get(field_loc, '')
            
        logging.info(f"Site : {data['nom_site']} - {data['date_mise_a_jour']}")
        # logging.info(f"Menages : {data['menages']}")
        logging.info(f"Individus : {data['individus']}")
        logging.info(f"Type de mouvement : {movement_type}")
        logging.info("-" * 20)
        
        # Ajout des données démographiques
        for field in MovementCalculator.DEMOGRAPHIC_FIELDS:
            record[field] = data.get(field, 0)
        
        return record

@api_view(["POST", "PUT"])
def import_data_cccm_from_excel_v2(request):
    """Import des données CCCM depuis un fichier Excel - Version améliorée"""
    
    service = DataImportService()
    
    try:
        # Validation du fichier
        file_data = request.FILES.get('file_data')
        if not file_data:
            return Response(
                {"message": "Le fichier de données est requis"}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        # Chargement du workbook
        try:
            wb = openpyxl.load_workbook(file_data, data_only=True, read_only=True)
        except Exception as e:
            return Response(
                {"message": f"Erreur lors du chargement du fichier Excel: {str(e)}"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Nettoyage des données existantes
        DataImport.objects.all().delete()
        logging.info("Données existantes supprimées")
        
        # Variables de suivi
        raw_stats = {}
        sites_data = defaultdict(list)
        total_raw_records = 0
        
        # Lecture des données depuis toutes les feuilles
        for sheet_name, default_date in service.SHEETS_CONFIG:
            if sheet_name not in wb.sheetnames:
                logging.warning(f"Feuille {sheet_name} non trouvée")
                continue
                
            sheet = wb[sheet_name]
            processed_data, sheet_count = service.process_sheet_data(
                sheet, sheet_name, default_date
            )
            
            raw_stats[sheet_name] = sheet_count
            total_raw_records += sheet_count
            
            # Groupement par site
            for data in processed_data:
                sites_data[data['nom_site']].append(data)
        
        # Tri des données de chaque site par date
        for site_name in sites_data:
            sites_data[site_name].sort(key=lambda x: x['date_mise_a_jour'])
        
        # Sauvegarde des enregistrements
        records_created = 0
        
        for site_name, site_records in sites_data.items():
            try:
                for index, record in enumerate(site_records):
                    logging.info(f"Index : {index}")
                    if index == 0:
                        # Premier enregistrement = donnée brute
                        raw_record = service.create_record_dict(record, "donnee_brute")
                        DataImport.objects.create(**raw_record)
                    else:
                        # Enregistrements suivants = mouvements calculés
                        new_record = service.processor.create_new_record(record)
                        if new_record is not None:
                            DataImport.objects.create(**new_record)
                    
                    records_created += 1
                    
            except Exception as e:
                logging.error(f"Erreur lors de la sauvegarde pour le site {site_name}: {e}")
                continue
        
        # Récupération des données sauvegardées
        all_data_in_db = DataImport.objects.all().order_by('date_mise_a_jour')
        data_serialized = DataImportSerializer(all_data_in_db, many=True)
        
        # Statistiques finales
        final_stats = {
            "raw_data_by_sheet": raw_stats,
            "total_raw_records": total_raw_records,
            "unique_sites": len(sites_data),
            "total_records_created": records_created,
            "sheets_processed": len([s for s in service.SHEETS_CONFIG if s[0] in wb.sheetnames])
        }
        
        response_data = {
            "stats": final_stats,
            "count": len(all_data_in_db),
            "data": data_serialized.data,
            "message": "Importation réussie"
        }
        
        logging.info(f"Importation terminée avec succès: {records_created} enregistrements créés")
        return Response(response_data, status=status.HTTP_200_OK)
        
    except Exception as e:
        logging.error(f"Erreur lors de l'importation: {e}")
        return Response(
            {"message": f"Erreur lors de l'importation: {str(e)}"}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['GET'])
def export_data_import_excel(request):
    """Export des données vers Excel"""
    try:
        # Récupération des données
        all_data_import = DataImport.objects.all().order_by("date_mise_a_jour")
        
        if not all_data_import.exists():
            return Response(
                {"message": "Aucune donnée à exporter"}, 
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Création du workbook
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "DONNEES 2023 - 2024 - 2025"

        # En-têtes
        headers = [
            "No",
            "PROVINCE", "CODE PROVINCE", "TERRITOIRE", "CODE TERRITOIRE", "ZONE SANTE", "CODE ZONE SANTE", 
            "NOM SITE", "CODE SITE", "TYPE SITE", "LONGITUDE", "LATITUDE", 
            "DATE", "TYPE MOUVEMENT", "MENAGES", "INDIVIDUS", 
            "0-4 F", "5-11 F", "12-17 F", "18-24 F", "25-59 F", "60+ F",
            "0-4 H", "5-11 H", "12-17 H", "18-24 H", "25-59 H", "60+ H"
        ]

        # Écriture des en-têtes
        ws.append(headers)
        for cell in ws[1]:
            cell.font = Font(bold=True)

        # Écriture des données
        for index, obj in enumerate(all_data_import):
            row = [
                index + 1,
                obj.province, obj.code_province, obj.territoire, obj.code_territoire, obj.zone_sante, obj.code_zone_sante,
                obj.nom_site, obj.code_site, obj.type_site, obj.longitude, obj.latitude,
                obj.date_mise_a_jour, obj.type_mouvement, obj.menages, obj.individus,
                obj.individus_0_4_f, obj.individus_5_11_f, obj.individus_12_17_f,
                obj.individus_18_24_f, obj.individus_25_59_f, obj.individus_60_f,
                obj.individus_0_4_h, obj.individus_5_11_h, obj.individus_12_17_h,
                obj.individus_18_24_h, obj.individus_25_59_h, obj.individus_60_h,
            ]
            ws.append(row)

        # Ajustement des colonnes
        for column in ws.columns:
            max_length = 0
            column_letter = get_column_letter(column[0].column)
            
            for cell in column:
                try:
                    if len(str(cell.value)) > max_length:
                        max_length = len(str(cell.value))
                except:
                    pass
            
            adjusted_width = min(max_length + 2, 50)  # Limite à 50 caractères
            ws.column_dimensions[column_letter].width = adjusted_width

        # Préparation de la réponse
        response = HttpResponse(
            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
        response["Content-Disposition"] = 'attachment; filename="data_import_cccm.xlsx"'
        
        wb.save(response)
        return response
        
    except Exception as e:
        logging.error(f"Erreur lors de l'export: {e}")
        return Response(
            {"message": f"Erreur lors de l'export: {str(e)}"}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['GET'])
def situation_par_site(request):
    """Calcule la situation actuelle par site"""
    try:
        # Récupération de toutes les données triées par date
        all_data = DataImport.objects.all().order_by("date_mise_a_jour")
        
        if not all_data.exists():
            return Response(
                {"message": "Aucune donnée disponible"}, 
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Initialisation des compteurs globaux
        totals = {
            'individus_restant': 0,
            'menages_restant': 0,
        }
        
        # Initialisation des compteurs démographiques
        for field in MovementCalculator.DEMOGRAPHIC_FIELDS:
            totals[field] = 0
        
        # Dictionnaire pour stocker les données par site
        sites = defaultdict(lambda: {key: 0 for key in totals.keys()})
        
        # Calcul des totaux cumulés
        for data in all_data:
            # Facteur multiplicateur selon le type de mouvement
            factor = 1 if data.type_mouvement in ["donnee_brute", "entree"] else -1
            
            # Mise à jour des totaux globaux
            totals['individus_restant'] += factor * data.individus
            totals['menages_restant'] += factor * data.menages
            
            # Mise à jour des totaux démographiques
            for field in MovementCalculator.DEMOGRAPHIC_FIELDS:
                totals[field] += factor * getattr(data, field, 0)
            
            # Sauvegarde de l'état actuel pour ce site
            sites[data.nom_site] = totals.copy()
        
        # Préparation de la réponse
        response = {
            **totals,
            'sites': dict(sites),
            'nombre_sites': len(sites),
            'derniere_mise_a_jour': all_data.last().date_mise_a_jour if all_data.exists() else None
        }
        
        return Response(response, status=status.HTTP_200_OK)
        
    except Exception as e:
        logging.error(f"Erreur lors du calcul de la situation par site: {e}")
        return Response(
            {"message": f"Erreur lors du calcul: {str(e)}"}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )