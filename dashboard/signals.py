from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.cache import cache
from .models import MouvementDeplace
from .views import CACHE_KEY_COORDINATEURS_GESTIONNAIRES, CACHE_KEY_DASHBOARD


@receiver([post_save, post_delete], sender=MouvementDeplace)
def clear_coordinateurs_gestionnaires_cache(sender, **kwargs):
    """
    Invalide le cache quand un MouvementDeplace est ajouté, modifié ou supprimé
    """
    cache.delete(CACHE_KEY_COORDINATEURS_GESTIONNAIRES)
    cache.delete(CACHE_KEY_DASHBOARD)
