from django.apps import AppConfig
import logging
import sys

logger = logging.getLogger(__name__)

class DashboardConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'dashboard'
    
    def ready(self):
        try:
            if any(cmd in sys.argv for cmd in ['runserver', 'gunicorn', 'uwsgi']) and not any(cmd in sys.argv for cmd in ['makemigrations', 'migrate', 'shell', 'check']):
                from .services import sync_service
                sync_service.start()
                logger.info("Service de synchronisation automatique activé")
                # Optionnel : sync_service.force_sync()
        except Exception as e:
            logger.error(f"Erreur lors du démarrage du service de synchronisation : {e}")
