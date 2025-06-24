from django.urls import path
from .views import UsuarioRegister, UsuarioLogin, UsuarioList, UsuarioDetail

urlpatterns = [
    path('register/', UsuarioRegister.as_view()),
    path('login/', UsuarioLogin.as_view()),
    path('usuario/', UsuarioList.as_view()),
    path('usuario/<str:usuario_id>/', UsuarioDetail.as_view()),
]
