from django import forms
from .models import SiteUnique, MouvementDeplaceSiteUnique


class MouvementDeplaceSiteUniqueForm(forms.ModelForm):
    mois = forms.ChoiceField(
        label="Mois",
        choices=MouvementDeplaceSiteUnique.MOIS_CHOICE,
        widget=forms.Select(
            attrs={
                "class": "mt-1 block w-full border border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500 text-sm"
            },
        ),
    )

    site = forms.ModelChoiceField(
        label="Site",
        queryset=SiteUnique.objects.all().order_by("nom"),
        widget=forms.Select(
            attrs={
                "class": "mt-1 block w-full border border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500 text-sm"
            }
        ),
    )

    menages = forms.IntegerField(
        label="Ménages",
        widget=forms.NumberInput(
            attrs={
                "class": "mt-1 block w-full border border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500 text-sm"
            }
        ),
    )

    individus = forms.IntegerField(
        label="Individus",
        widget=forms.NumberInput(
            attrs={
                "class": "mt-1 block w-full border border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500 text-sm"
            }
        ),
    )

    class Meta:
        model = MouvementDeplaceSiteUnique
        fields = ("mois", "site", "menages", "individus")
