from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from rest_framework.routers import DefaultRouter
from . import views
from .views import UsuarioViewSet
from .views import fake_token_obtain_pair

router = DefaultRouter()
router.register(r'usuarios', UsuarioViewSet, basename='usuario')

urlpatterns = [
    path('', include(router.urls)),
    
    # Endpoints para zonas
    path('zonas/', views.lista_zonas, name='lista-zonas'),
    path('zonas/<str:zona_id>/', views.detalle_zona, name='detalle-zona'),
    
    # Endpoints para lecturas por zona
    path('zonas/<str:zona_id>/lecturas/', views.lecturas_por_zona, name='lecturas-por-zona'),
    
    # Endpoints para nodos
    path('zonas/<str:zona_id>/nodos/', views.nodos_por_zona, name='nodos-por-zona'),
    
    # Endpoints para sensores
    path('nodos/<str:nodo_id>/sensores/', views.sensores_por_nodo, name='sensores-por-nodo'),
    
    # Endpoints para lecturas por sensor
    path('sensores/<str:sensor_id>/lecturas/', views.lecturas_por_sensor, name='lecturas-por-sensor'),

    path('datos/', views.registrar_datos, name='registrar_datos'),

    path("api/ultima_humedad/", views.obtener_humedad, name="obtener_humedad"),

    path("api/ultima_temperatura/", views.obtener_temperatura, name="obtener_temperatura"),

    path("api/ultima_flujo/", views.obtener_flujo, name="obtener_flujo"),

    path("api/ultimo_id/", views.ultimo_id, name="ultimo_id"),
    
    # Endpoints para JWT
    # path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/', fake_token_obtain_pair, name='fake_token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
] 