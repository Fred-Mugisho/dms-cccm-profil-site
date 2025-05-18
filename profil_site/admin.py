from django.contrib import admin
from .models import *
from django.contrib.auth.models import Group

admin.site.unregister(Group)

models_list = [
    InformationGeneraleProfilSite,
    GestionSite,
    WashSite,
    SanteSite,
]
for model in models_list:
    admin.site.register(model)