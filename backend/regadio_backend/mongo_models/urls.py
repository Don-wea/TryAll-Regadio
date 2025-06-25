# from django.urls import path, include
# from rest_framework import routers
# from .views import (
#     ZonaRiegoViewSet, NodoViewSet, SensorViewSet, RegadorViewSet,
#     ConfiguracionRiegoViewSet, SugerenciaViewSet, LecturaSensorViewSet, RegistroRiegoViewSet
# )
# from .views import (    UsuarioRegister, UsuarioLogin, UsuarioList, UsuarioDetail
# )

# router = routers.DefaultRouter()
# # router.register(r'usuarios', UsuarioViewSet, basename='usuario')
# router.register(r'zonas', ZonaRiegoViewSet, basename='zona')
# router.register(r'nodos', NodoViewSet, basename='nodo')
# router.register(r'sensores', SensorViewSet, basename='sensor')
# router.register(r'regadores', RegadorViewSet, basename='regador')
# router.register(r'configuraciones-riego', ConfiguracionRiegoViewSet, basename='configuracion-riego')
# router.register(r'sugerencias', SugerenciaViewSet, basename='sugerencia')
# router.register(r'lecturas', LecturaSensorViewSet, basename='lectura')
# router.register(r'registros-riego', RegistroRiegoViewSet, basename='registro-riego')

# urlpatterns = [
#     # path('crud/', include(router.urls)),

#     path('register/', UsuarioRegister.as_view()),
#     path('login/', UsuarioLogin.as_view()),
#     path('usuario/', UsuarioList.as_view()),
#     path('usuario/<str:usuario_id>/', UsuarioDetail.as_view()),

# ]
