# riego_api/apps.py

from django.apps import AppConfig
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

class RiegoApiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'riego_api'

    def ready(self):
        if settings.MODO_TEST:
            from .data_loader import cargar_datos_fake
            self.fake_data = cargar_datos_fake()
            logger.info("Modo test activado: datos fake cargados.")
