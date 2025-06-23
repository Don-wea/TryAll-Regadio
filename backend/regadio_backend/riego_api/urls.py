from django.urls import path
from . import views

urlpatterns = [
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

    path('api/humedad/', views.humedad_ultima, name='registrar_humedad'),

    path("api/ultima_humedad/", views.obtener_humedad, name="obtener_humedad"),

    path("enviar_flujo/", views.recibir_cantidad_flujo, name="recibir_flujo"),

    path("recibir_flujo/", views.enviar_cantidad_flujo, name="enviar_flujo"),

    path("api/ultima_temperatura/", views.obtener_temperatura, name="obtener_temperatura"),

    path("api/ultima_flujo/", views.obtener_flujo, name="obtener_flujo"),

    path("api/ultimo_id/", views.ultimo_id, name="ultimo_id"),
]