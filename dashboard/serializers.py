from rest_framework import serializers
from .models import *

class CoordonneesSiteSerializer(serializers.ModelSerializer):
    class Meta:
        model = CoordonneesSite
        fields = '__all__'