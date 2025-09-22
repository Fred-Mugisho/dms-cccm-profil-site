from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.cache import cache
from data_import.models import SiteDeplace
from .models import MouvementDeplace
from .views import CACHE_KEY_COORDINATEURS_GESTIONNAIRES, CACHE_KEY_DASHBOARD


@receiver([post_save, post_delete], sender=MouvementDeplace)
def clear_dashboard_cache(sender, **kwargs):
    cache.delete(CACHE_KEY_DASHBOARD)
    
@receiver([post_save, post_delete], sender=SiteDeplace)
def clear_coordinateurs_gestionnaires_cache(sender, **kwargs):
    cache.delete(CACHE_KEY_COORDINATEURS_GESTIONNAIRES)
