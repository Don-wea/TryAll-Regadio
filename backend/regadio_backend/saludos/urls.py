from django.urls import path
from . import views

urlpatterns = [
    path('saludo/', views.obtener_saludo, name='obtener_saludo'),
]