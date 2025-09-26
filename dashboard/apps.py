from django.apps import AppConfig
import logging
import sys
from django.db.models.signals import post_migrate

logger = logging.getLogger(__name__)

class DashboardConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'dashboard'
    
    def ready(self):
        import dashboard.signals # noqa
        try:
            if any(cmd in sys.argv for cmd in ['runserver', 'gunicorn', 'uwsgi']) and not any(cmd in sys.argv for cmd in ['makemigrations', 'migrate', 'shell', 'check']):
                from .services import sync_service
                post_migrate.connect(lambda **kwargs: sync_service.start(), sender=self)
                # sync_service.start()
                logger.info("Service de synchronisation automatique activé")
                # Optionnel : sync_service.force_sync()
        except Exception as e:
            logger.error(f"Erreur lors du démarrage du service de synchronisation : {e}")
