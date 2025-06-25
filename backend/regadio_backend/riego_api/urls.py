from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from django.views.decorators.csrf import csrf_exempt
from rest_framework.routers import DefaultRouter
from . import views
from .views import UsuarioViewSet
from .views import fake_token_obtain_pair
from .views import chat_with_gemini
from .views import (    
    UsuarioRegister, 
    UsuarioLogin, 
    UsuarioList, 
    UsuarioDetail
)

router = DefaultRouter()
router.register(r'usuarios', UsuarioViewSet, basename='usuario')

urlpatterns = [
    path('', include(router.urls)),
    
    #AI
    path('chat/', csrf_exempt(chat_with_gemini), name='chat_with_gemini'),
    # Endpoints para zonas
    path('zonas/', views.lista_zonas, name='lista-zonas'),
    path('zonas/<str:zona_id>/', views.detalle_zona, name='detalle-zona'),
    path('zonas/<str:zona_id>/lecturas/', views.lecturas_por_zona, name='lecturas-por-zona'),
    path('zonas/<str:zona_id>/nodos/', views.nodos_por_zona, name='nodos-por-zona'),
    path('nodos/<str:nodo_id>/sensores/', views.sensores_por_nodo, name='sensores-por-nodo'),
    path('sensores/<str:sensor_id>/lecturas/', views.lecturas_por_sensor, name='lecturas-por-sensor'),

    path('datos/', views.registrar_datos, name='registrar_datos'),
    path('api/humedad/', views.humedad_ultima, name='registrar_humedad'),
    path("api/ultima_humedad/", views.obtener_humedad, name="obtener_humedad"),
    path("enviar_flujo/", views.recibir_cantidad_flujo, name="recibir_flujo"),
    path("recibir_flujo/", views.enviar_cantidad_flujo, name="enviar_flujo"),

    path("enviar_flujo_actual/", views.obtener_flujo_actual, name="enviar_flujo_actual"),

    path("recibir_flujo_actual/", views.retornar_flujo_actual, name="recibir_flujo_actual"),

    path("enviar_humedad_y_temperatura/", views.recibir_humedad_y_temperatura, name="enviar_humedad_y_temperatura"),
    path("recibir_humedad_y_temperatura/", views.enviar_humedad_y_temperatura, name="recibir_humedad_y_temperatura/"),
    path('guardar_humedad_temperatura/', views.guardar_humedad_temperatura, name='guardar_humedad_temperatura'),
    


    path("api/ultima_temperatura/", views.obtener_temperatura, name="obtener_temperatura"),
    path("api/ultima_flujo/", views.obtener_flujo, name="obtener_flujo"),

    path("api/ultimo_id/", views.enviar_ultimo_id, name="ultimo_id"),

    path("api/enviar_ultimo_id/", views.recibir_ultimo_id, name="recibir_ultimo_id"),

    #enviar flujo,guardad humedad y guardar temperatura
    path("enviar_flujoabd/", views.guardar_flujo_objetivo, name="guardar_flujo_objetivo"),
    path("guardar_humedad/", views.guardar_humedad, name="guardar_humedad"),              # POST: guarda humedad
    path("guardar_temperatura/", views.guardar_temperatura, name="guardar_temperatura"),  # POST: guarda temperatura

    # Endpoints de datos historicos
    #regadores
    path('datos_historicos/ultimos_flujos/<int:cantidad>/', views.historicos_ultimos_flujos, name='ultimos_flujos'), # registros de riego
    #sensores
    path('datos_historicos/ultimas_humedades/<int:cantidad>/', views.historicos_ultimas_humedades, name='ultimas_humedades'),  # lectura sensor - humedad
    path('datos_historicos/ultimas_temperaturas/<int:cantidad>/', views.historicos_ultimas_temperaturas, name='ultimas_temperaturas'),  # lectura sensor - temperatura

    # Endpoints para JWT
    # path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/', fake_token_obtain_pair, name='fake_token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('register/', UsuarioRegister.as_view()),
    path('login/', UsuarioLogin.as_view()),
    path('usuario/', UsuarioList.as_view()),
    path('usuario/<str:usuario_id>/', UsuarioDetail.as_view()),
]
