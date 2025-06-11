from django.conf import settings
from django.apps import apps
from bson import ObjectId

class DataRepository:
    """
    Repositorio que maneja el acceso a datos, ya sea desde MongoDB o desde los datos fake
    cuando MODO_TEST=1
    """
    
    @staticmethod
    def get_all(model_class):
        """
        Obtiene todos los objetos de un modelo específico
        """
        if settings.MODO_TEST:
            # Obtener los datos fake desde la app
            app_config = apps.get_app_config('riego_api')
            collection_name = model_class._meta.get('collection', model_class.__name__.lower() + 's')
            return getattr(app_config.fake_data, collection_name, [])
        else:
            # Usar MongoDB normalmente
            return model_class.objects.all()
    
    @staticmethod
    def get_by_id(model_class, object_id):
        """
        Obtiene un objeto por su ID
        """
        if settings.MODO_TEST:
            app_config = apps.get_app_config('riego_api')
            collection_name = model_class._meta.get('collection', model_class.__name__.lower() + 's')
            collection = getattr(app_config.fake_data, collection_name, [])
            
            # Buscar el objeto por ID
            for obj in collection:
                if str(obj._id) == str(object_id):
                    return obj
            return None
        else:
            # Usar MongoDB normalmente
            return model_class.objects.get(id=object_id)
    
    @staticmethod
    def filter(model_class, **kwargs):
        """
        Filtra objetos según los criterios proporcionados
        """
        if settings.MODO_TEST:
            app_config = apps.get_app_config('riego_api')
            collection_name = model_class._meta.get('collection', model_class.__name__.lower() + 's')
            collection = getattr(app_config.fake_data, collection_name, [])
            
            # Filtrar objetos según los criterios
            result = []
            for obj in collection:
                match = True
                for key, value in kwargs.items():
                    # Manejar campos de referencia (por ejemplo, zona_id=zona)
                    if key.endswith('_id') and hasattr(obj, key) and hasattr(value, '_id'):
                        if getattr(obj, key)._id != value._id:
                            match = False
                            break
                    elif getattr(obj, key, None) != value:
                        match = False
                        break
                if match:
                    result.append(obj)
            return result
        else:
            # Usar MongoDB normalmente
            return model_class.objects.filter(**kwargs)