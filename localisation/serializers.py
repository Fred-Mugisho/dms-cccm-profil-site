from .models import *
from rest_framework import serializers

class PositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Position
        fields = ['id', 'latitude', 'longitude', 'altitude', 'precision']
        
class LocalisationSerializer(serializers.ModelSerializer):
    position = PositionSerializer()
    enfants = serializers.SerializerMethodField()
    class Meta:
        model = Localisation
        fields = ['id', 'type', 'nom', 'code', 'position', 'enfants']
        
    def get_enfants(self, obj):
        return LocalisationSerializer(obj.enfants.all(), many=True).data
    
class SimpleLocalisationSerializer(serializers.ModelSerializer):
    position = PositionSerializer()
    class Meta:
        model = Localisation
        fields = ['id', 'type', 'nom', 'code', 'position']
    
class LocalisationFormSerializer(serializers.ModelSerializer):
    class Meta:
        model = Localisation
        fields = ['id', 'type', 'nom', 'code', 'parent', 'position']