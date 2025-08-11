from rest_framework import serializers
from .models import SiteDeplace, MouvementDeplace, SiteUnique, MouvementDeplaceSiteUnique


class SiteDeplaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = SiteDeplace
        fields = '__all__'
        

class MouvementDeplaceSerializer(serializers.ModelSerializer):
    site = SiteDeplaceSerializer()
    class Meta:
        model = MouvementDeplace
        fields = '__all__'

class SiteUniqueSerializer(serializers.ModelSerializer):
    class Meta:
        model = SiteUnique
        fields = ['id', 'nom']
        
class MouvementDeplaceSiteUniqueSerializer(serializers.ModelSerializer):
    site = SiteUniqueSerializer()
    class Meta:
        model = MouvementDeplaceSiteUnique
        fields = "__all__"