from data_import.models import SiteDeplace
from django.db import models
from rest_framework import serializers
from .base_model import BaseModel
from data_import.serializers import SiteDeplaceSerializer

class ProfilSite(BaseModel):
    site = models.ForeignKey(SiteDeplace, on_delete=models.CASCADE, db_index=True)
    enqueteur = models.CharField(max_length=255)
    organisation = models.CharField(max_length=255)
    concerne_nouveau_site = models.BooleanField(default=False)
    nombre_menages = models.PositiveBigIntegerField(default=0)
    nombre_individus = models.PositiveBigIntegerField(default=0)
    
    # Personnes par groupe d'age et sexe
    individus_0_4_f = models.PositiveBigIntegerField(default=0)
    individus_5_11_f = models.PositiveBigIntegerField(default=0)
    individus_12_17_f = models.PositiveBigIntegerField(default=0)
    individus_18_24_f = models.PositiveBigIntegerField(default=0)
    individus_25_59_f = models.PositiveBigIntegerField(default=0)
    individus_60_f = models.PositiveBigIntegerField(default=0)
    individus_0_4_h = models.PositiveBigIntegerField(default=0)
    individus_5_11_h = models.PositiveBigIntegerField(default=0)
    individus_12_17_h = models.PositiveBigIntegerField(default=0)
    individus_18_24_h = models.PositiveBigIntegerField(default=0)
    individus_25_59_h = models.PositiveBigIntegerField(default=0)
    individus_60_h = models.PositiveBigIntegerField(default=0)
    
    statut_site = models.CharField(max_length=255) # Fonctionnel ou non fonctionnel
    
    def __str__(self):
        return self.site.nom_site
    
class ProfilSiteSerializer(serializers.ModelSerializer):
    site = SiteDeplaceSerializer()
    class Meta:
        model = ProfilSite
        fields = '__all__'
        
class FormProfilSiteSerializer(serializers.ModelSerializer):
    nouveau_site = SiteDeplaceSerializer(required=False)
    code_site = serializers.CharField(required=False)
    class Meta:
        model = ProfilSite
        fields = '__all__'
        extra_kwargs = {
            'site': {'read_only': True}
        }
        
    def create(self, validated_data):
        code_site = validated_data.pop('code_site', None)
        concerne_nouveau_site = validated_data.get('concerne_nouveau_site', False)
        nouveau_site_data = validated_data.pop('nouveau_site', None)
        
        # Se rassure que nombre_individus == au somme de tous les groupes d'age et sexe
        nombre_individus = validated_data.get("nombre_individus", 0)
        nombre_individus_groupes = (
            validated_data.get('individus_0_4_f', 0) +
            validated_data.get('individus_5_11_f', 0) +
            validated_data.get('individus_12_17_f', 0) +
            validated_data.get('individus_18_24_f', 0) +
            validated_data.get('individus_25_59_f', 0) +
            validated_data.get('individus_60_f', 0) +
            validated_data.get('individus_0_4_h', 0) +
            validated_data.get('individus_5_11_h', 0) +
            validated_data.get('individus_12_17_h', 0) +
            validated_data.get('individus_18_24_h', 0) +
            validated_data.get('individus_25_59_h', 0) +
            validated_data.get('individus_60_h', 0)
        )
        if nombre_individus != nombre_individus_groupes:
            raise serializers.ValidationError({
                "nombre_individus": "Le nombre d'individus doit correspondre au somme de tous les groupes d'age et sexe."
            })
        
        # Cas d’un nouveau site
        
        if concerne_nouveau_site:
            if not nouveau_site_data:
                raise serializers.ValidationError({
                    "nouveau_site": "Les informations du nouveau site sont obligatoires si 'concerne_nouveau_site' est vrai."
                })
                
            # Création du nouveau site
            site = SiteDeplace.objects.create(**nouveau_site_data)
            return ProfilSite.objects.create(site=site, **validated_data)
        
        # Cas d’un site existant
        if not code_site:
            raise serializers.ValidationError({
                "code_site": "Vous devez fournir un code_site si 'concerne_nouveau_site' est faux."
            })
            
        site = SiteDeplace.objects.filter(code_site=code_site).first()
        if not site:
            raise serializers.ValidationError({
                "code_site": f"Aucun site trouvé avec le code '{code_site}'."
            })
        
        return ProfilSite.objects.create(site=site, **validated_data)