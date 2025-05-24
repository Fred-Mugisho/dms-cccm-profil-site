from .models import *
from rest_framework import serializers

class ProvinceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Province
        fields = ['id', 'name', 'code', 'territoires', 'zones_sante']
        read_only_fields = ['territoires', 'zones_sante']
        
class ProvinceFormSerializer(serializers.ModelSerializer):
    class Meta:
        model = Province
        fields = ['id', 'name', 'code']
        
class TerritoireSerializer(serializers.ModelSerializer):
    class Meta:
        model = Territoire
        fields = ['id', 'name', 'code', 'secteurs']
        read_only_fields = ['secteurs']
        
class TerritoireFormSerializer(serializers.ModelSerializer):
    class Meta:
        model = Territoire
        fields = ['id', 'province', 'name', 'code']
        
class SecteurSerializer(serializers.ModelSerializer):
    class Meta:
        model = Secteur
        fields = ['id', 'name', 'code', 'groupements']
        read_only_fields = ['groupements']
        
class SecteurFormSerializer(serializers.ModelSerializer):
    class Meta:
        model = Secteur
        fields = ['id', 'territoire', 'name', 'code']
        
class GroupementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Groupement
        fields = ['id', 'name', 'code', 'villages']
        read_only_fields = ['villages']
        
class GroupementFormSerializer(serializers.ModelSerializer):
    class Meta:
        model = Groupement
        fields = ['id', 'secteur', 'name', 'code']
        
class VillageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Village
        fields = ['id', 'name', 'code']
        
class VillageFormSerializer(serializers.ModelSerializer):
    class Meta:
        model = Village
        fields = ['id', 'groupement', 'name', 'code']
        
class ZoneSanteSerializer(serializers.ModelSerializer):
    province = ProvinceSerializer()
    class Meta:
        model = ZoneSante
        fields = ['id', 'name', 'code', 'province']
        read_only_fields = ['province']
        
class ZoneSanteFormSerializer(serializers.ModelSerializer):
    class Meta:
        model = ZoneSante
        fields = ['id', 'province', 'name', 'code']
        
class AireSanteSerializer(serializers.ModelSerializer):
    class Meta:
        model = AireSante
        fields = ['id', 'name', 'code']
        
class AireSanteFormSerializer(serializers.ModelSerializer):
    class Meta:
        model = AireSante
        fields = ['id', 'zone_sante', 'name', 'code']
        
class LimiteAdministrativeSerializer(serializers.ModelSerializer):
    class Meta:
        model = LimiteAdministrative
        fields = ['id', 'name', 'code', 'level', 'latitude', 'longitude', 'limite', 'children']
        read_only_fields = ['children']
        
class LimiteAdministrativeFormSerializer(serializers.ModelSerializer):
    class Meta:
        model = LimiteAdministrative
        fields = ['id', 'parent', 'name', 'code', 'level', 'latitude', 'longitude', 'limite']