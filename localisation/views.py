from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from utils.functions import validate_level_location
from .models import *
from .serializers import *


@api_view(['GET'])
def localisations(request):
    try:
        localisations = Localisation.objects.filter(parent__isnull=True).order_by('nom')
        serializer = LocalisationSerializer(localisations, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
@api_view(['GET'])
def get_localisation(request, id):
    try:
        localisation = Localisation.objects.get(id=id)
        parent = SimpleLocalisationSerializer(localisation.parent).data
        serializer = LocalisationSerializer(localisation).data
        serializer['parent'] = parent
        return Response(serializer, status=status.HTTP_200_OK)
    except Localisation.DoesNotExist:
        return Response({"message": "Localisation n'existe pas"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
@api_view(['POST', 'PUT'])
def create_update_localisation(request, id=None):
    try:
        localisation = Localisation.objects.get(id=id) if id else None
        type = request.data.get('type')
        nom = request.data.get('nom')
        parent = request.data.get('parent')
        position_data = request.data.get('position')
                
        parent_instance = Localisation.objects.get(id=parent) if parent else None
        
        statut, error = validate_level_location(type, parent_instance)
        if not statut:
            return Response({"message": error}, status=status.HTTP_400_BAD_REQUEST)
        
        if position_data:
            position_form = PositionSerializer(localisation.position if localisation else None, data=position_data)
            if position_form.is_valid():
                position = position_form.save()
            else:
                return Response(position_form.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            position = localisation.position if localisation else None
        
        data_location = {
            'type': type,
            'nom': nom,
            'parent': parent_instance.pk if parent_instance else None,
            'position': position.pk if position else None,
        }
        localisation_form = LocalisationFormSerializer(localisation, data=data_location)
        if localisation_form.is_valid():
            location = localisation_form.save()
            serialiser = LocalisationSerializer(location)
            return Response(serialiser.data, status=status.HTTP_200_OK)
        else:
            return Response(localisation_form.errors, status=status.HTTP_400_BAD_REQUEST)
    except Localisation.DoesNotExist:
        return Response({"message": "Localisation n'existe pas"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

