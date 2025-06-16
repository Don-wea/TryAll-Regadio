from django.urls import path, include
from rest_framework import routers
from .views import (
    UsuarioViewSet, ZonaRiegoViewSet, NodoViewSet, SensorViewSet, RegadorViewSet,
    ConfiguracionRiegoViewSet, SugerenciaViewSet, LecturaSensorViewSet, RegistroRiegoViewSet
)

router = routers.DefaultRouter()
router.register(r'usuarios', UsuarioViewSet, basename='usuario')
# router.register(r'zonas', ZonaRiegoViewSet)
# router.register(r'nodos', NodoViewSet)
# router.register(r'sensores', SensorViewSet)
# router.register(r'regadores', RegadorViewSet)
# router.register(r'configuraciones-riego', ConfiguracionRiegoViewSet)
# router.register(r'sugerencias', SugerenciaViewSet)
# router.register(r'lecturas', LecturaSensorViewSet)
# router.register(r'registros-riego', RegistroRiegoViewSet)

urlpatterns = [
    path('crud/', include(router.urls)),
]
