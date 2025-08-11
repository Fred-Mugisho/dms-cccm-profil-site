from django.contrib import admin
from .models import SiteUnique, MouvementDeplaceSiteUnique, SiteDeplace

admin.site.register([
    SiteUnique,
    MouvementDeplaceSiteUnique,
    SiteDeplace
])