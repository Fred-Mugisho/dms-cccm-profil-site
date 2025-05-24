from django.contrib import admin
from .models import *

models_list = [
    Province, Territoire, Secteur, Groupement, Village, ZoneSante, AireSante, LimiteAdministrative
]

for model in models_list:
    admin.site.register(model)