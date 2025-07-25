from rest_framework import serializers
from .models import SiteDeplace, MouvementDeplace


class SiteDeplaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = SiteDeplace
        fields = '__all__'
        

class MouvementDeplaceSerializer(serializers.ModelSerializer):
    site = SiteDeplaceSerializer()
    class Meta:
        model = MouvementDeplace
        fields = '__all__'
