from .models import *
from rest_framework import serializers

class ProvinceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Province
        fields = ['id', 'name', 'code', 'territoires']
        read_only_fields = ['territoires']
        
class ProvinceFormSerializer(serializers.ModelSerializer):
    class Meta:
        model = Province
        fields = ['id', 'name', 'code']
        
class TerritoireSerializer(serializers.ModelSerializer):
    class Meta:
        model = Territoire
        fields = ['id', 'name', 'code', 'secteurs', 'zones_sante']
        read_only_fields = ['secteurs', 'zones_sante']
        
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
        fields = ['id', 'name', 'code', 'latitude', 'longitude']
        
class VillageFormSerializer(serializers.ModelSerializer):
    class Meta:
        model = Village
        fields = ['id', 'groupement', 'name', 'code', 'latitude', 'longitude']
        
class ZoneSanteSerializer(serializers.ModelSerializer):
    class Meta:
        model = ZoneSante
        fields = ['id', 'name', 'code', 'aires_sante', 'latitude', 'longitude']
        
class ZoneSanteFormSerializer(serializers.ModelSerializer):
    class Meta:
        model = ZoneSante
        fields = ['id', 'province', 'name', 'code', 'latitude', 'longitude']
        
class AireSanteSerializer(serializers.ModelSerializer):
    class Meta:
        model = AireSante
        fields = ['id', 'name', 'code', 'latitude', 'longitude']
        
class AireSanteFormSerializer(serializers.ModelSerializer):
    class Meta:
        model = AireSante
        fields = ['id', 'zone_sante', 'name', 'code', 'latitude', 'longitude']
        
class LimiteAdministrativeSerializer(serializers.ModelSerializer):
    class Meta:
        model = LimiteAdministrative
        fields = ['id', 'name', 'code', 'level', 'latitude', 'longitude', 'limite', 'children']
        read_only_fields = ['children']
        
class LimiteAdministrativeFormSerializer(serializers.ModelSerializer):
    class Meta:
        model = LimiteAdministrative
        fields = ['id', 'parent', 'name', 'code', 'level', 'latitude', 'longitude', 'limite']
        
class DataImportSerializer(serializers.ModelSerializer):
    class Meta:
        model = DataImport
        fields = '__all__'
        
class TemporalDataImportSerializer(serializers.ModelSerializer):
    class Meta:
        model = TemporalDataImport
        fields = '__all__'