from django.contrib import admin
from .models import SiteUnique, MouvementDeplaceSiteUnique

admin.site.register([
    SiteUnique,
    MouvementDeplaceSiteUnique
])