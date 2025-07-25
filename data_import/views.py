from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import *
from django.http import HttpResponse
from django.db import transaction
import openpyxl
from openpyxl.utils import get_column_letter
from openpyxl.styles import Font
from utils.functions import *
from .utils import DataImportService


@api_view(['POST'])
def import_data(request):
    """Import des données CCCM depuis un fichier Excel - avec sécurité transactionnelle"""
    try:
        service = DataImportService()
        file_data = request.FILES.get('file_data')

        if not file_data:
            return Response({"message": "Le fichier de données est requis"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            wb = openpyxl.load_workbook(file_data, data_only=True, read_only=True)
        except Exception as e:
            return Response({"message": f"Erreur lors du chargement du fichier Excel: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)

        with transaction.atomic():  # ⛔ Début du bloc atomique
            # Nettoyage des anciens imports
            TemporalMouvementDeplace.objects.all().delete()
            MouvementDeplace.objects.all().delete()
            logging.info("Anciennes données supprimées.")
            
            print("Lecture des feuilles Excel...")

            # Lecture et traitement des feuilles Excel
            for sheet_name, default_date in service.SHEETS_CONFIG:
                if sheet_name not in wb.sheetnames:
                    logging.warning(f"Feuille {sheet_name} non trouvée")
                    continue

                sheet = wb[sheet_name]

                service.process_sheet_data_v3(sheet, sheet_name, default_date)
                
            variation_result = service.generate_variation_data()
            logging.info(f"Variations: {variation_result}")

            logging.info("Importation terminée.")

        return Response(service.statistiques(), status=status.HTTP_200_OK)
    except Exception as e:
        logging.error(f"Erreur lors de l'importation: {e}")
        return Response({"message": f"Erreur lors de l'importation: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
@api_view(['GET'])
def export_data(request):
    try:
        mouvements = MouvementDeplace.objects.all().order_by('date_mise_a_jour')
        logging.info(f"Nombre de mouvements trouvés: {mouvements.count()}")
        if not mouvements.exists():
            return Response(
                {"message": "Aucune donnée à exporter"}, 
                status=status.HTTP_404_NOT_FOUND
            )
            
        # Création du workbook
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "DONNEES 2023 - 2024 - 2025"
        
        entrees_individus = 0
        sortie_individus = 0

        # En-têtes
        headers = [
            "No",
            "PROVINCE", "CODE PROVINCE", "TERRITOIRE", "CODE TERRITOIRE", "ZONE SANTE", "CODE ZONE SANTE", 
            "NOM SITE", "CODE SITE", "TYPE SITE", "LONGITUDE", "LATITUDE", 
            "DATE", "TYPE MOUVEMENT", "MENAGES", "INDIVIDUS", 
            "0-4 F", "5-11 F", "12-17 F", "18-24 F", "25-59 F", "60+ F",
            "0-4 H", "5-11 H", "12-17 H", "18-24 H", "25-59 H", "60+ H",
            "PERSONNES VIVANT AVEC UN HANDICAP", "SOUS MECANISME CCCM"
        ]
        
        # Écriture des en-têtes
        ws.append(headers)
        for cell in ws[1]:
            cell.font = Font(bold=True)
            
        # Écriture des données
        for index, obj in enumerate(mouvements):
            mecanisme = 1 if obj.site.sous_mecanisme else 0
            row = [
                index + 1,
                obj.site.province, obj.site.code_province, obj.site.territoire, obj.site.code_territoire, obj.site.zone_sante, 
                obj.site.code_zone_sante, obj.site.nom_site, obj.site.code_site, obj.site.type_site, obj.site.longitude, 
                obj.site.latitude, obj.date_mise_a_jour, obj.type_mouvement, obj.menages, obj.individus, 
                obj.individus_0_4_f, obj.individus_5_11_f, obj.individus_12_17_f, obj.individus_18_24_f, obj.individus_25_59_f, 
                obj.individus_60_f, obj.individus_0_4_h, obj.individus_5_11_h, obj.individus_12_17_h, obj.individus_18_24_h, 
                obj.individus_25_59_h, obj.individus_60_h, obj.pvh, mecanisme
            ]
            ws.append(row)
            
            if obj.type_mouvement == 'entree':
                entrees_individus += obj.individus
            else:
                sortie_individus += obj.individus
            
        logging.info(f"Exportation terminee. Nombre de lignes: {index + 1}")
        
        logging.info(f"Entrees individus: {entrees_individus} - Sortie individus: {sortie_individus} - Différence: {entrees_individus - sortie_individus}")
            
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
            
        logging.info(f"Exportation terminee. Nombre de lignes: {index + 1}")

        # Préparation de la réponse
        response = HttpResponse(
            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
        response["Content-Disposition"] = 'attachment; filename="data_importable_cccm.xlsx"'
        
        wb.save(response)
        return response
    except Exception as e:
        logging.error(f"Erreur lors de l'exportation: {e}")
        return Response({"message": f"Erreur lors de l'exportation: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)