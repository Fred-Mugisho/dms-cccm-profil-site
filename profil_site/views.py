from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import *
from .serializers import *

@api_view(['GET'])
def profils_sites(request, id=None):
    try:
        if id:
            profil = InformationGeneraleProfilSite.objects.get(id=id)
            serializer = InformationGeneraleProfilSiteSerializer(profil)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            profils = InformationGeneraleProfilSite.objects.all().order_by('nom_site')
            serializer = InformationGeneraleProfilSiteSerializer(profils, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
    except InformationGeneraleProfilSite.DoesNotExist:
        return Response({"message": "Profil du site n'existe pas"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
@api_view(['POST', 'PUT'])
def create_profil_site(request):
    try:
        # Information Generale
        information_generale_data = request.data.get('information_generale')
        gestion_site_data = request.data.get('gestion_site')
        wash_site_data = request.data.get('wash_site')
        sante_site_data = request.data.get('sante_site')
        
        profil = InformationGeneraleProfilSite.objects.filter(siteId=information_generale_data.get('siteId')).first()
        if profil:
            gestion_site = GestionSite.objects.filter(profil=profil).first()
            wash_site = WashSite.objects.filter(profil=profil).first()
            sante_site = SanteSite.objects.filter(profil=profil).first()
        else:
            gestion_site = None
            wash_site = None
            sante_site = None
            
        information_generale_form = InformationGeneraleProfilSiteSerializer(profil, data=information_generale_data) if profil else InformationGeneraleProfilSiteSerializer(data=information_generale_data)
        if information_generale_form.is_valid():
            information_generale = information_generale_form.save()
            if gestion_site_data:
                gestion_site_data['profil'] = information_generale.pk
                gestion_site_form = GestionSiteSerializer(gestion_site, data=gestion_site_data) if gestion_site else GestionSiteSerializer(data=gestion_site_data)
                if gestion_site_form.is_valid():
                    gestion_site_form.save()
                else:
                    return Response(gestion_site_form.errors, status=status.HTTP_400_BAD_REQUEST)
            if wash_site_data:
                wash_site_data['profil'] = information_generale.pk
                wash_site_form = WashSiteSerializer(wash_site, data=wash_site_data) if wash_site else WashSiteSerializer(data=wash_site_data)
                if wash_site_form.is_valid():
                    wash_site_form.save()
                else:
                    return Response(wash_site_form.errors, status=status.HTTP_400_BAD_REQUEST)
            if sante_site_data:
                sante_site_data['profil'] = information_generale.pk
                sante_site_form = SanteSiteSerializer(sante_site, data=sante_site_data) if sante_site else SanteSiteSerializer(data=sante_site_data)
                if sante_site_form.is_valid():
                    sante_site_form.save()
                else:
                    return Response(sante_site_form.errors, status=status.HTTP_400_BAD_REQUEST)
            return Response({"message": "Profil du site créé avec succès"}, status=status.HTTP_201_CREATED)
        else:
            return Response(information_generale_form.errors, status=status.HTTP_400_BAD_REQUEST)
    except InformationGeneraleProfilSite.DoesNotExist:
        return Response({"message": "Profil du site n'existe pas"}, status=status.HTTP_404_NOT_FOUND)
    except GestionSite.DoesNotExist:
        return Response({"message": "Gestion du site n'existe pas"}, status=status.HTTP_404_NOT_FOUND)
    except WashSite.DoesNotExist:
        return Response({"message": "Wash du site n'existe pas"}, status=status.HTTP_404_NOT_FOUND)
    except SanteSite.DoesNotExist:
        return Response({"message": "Santé du site n'existe pas"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
