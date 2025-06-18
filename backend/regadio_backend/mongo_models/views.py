from rest_framework_mongoengine import viewsets
from .models import Usuario, ZonaRiego, Nodo, Sensor, Regador, ConfiguracionRiego, Sugerencia, LecturaSensor, RegistroRiego

from .serializers import UsuarioSerializer, ZonaRiegoSerializer, NodoSerializer, SensorSerializer, RegadorSerializer, ConfiguracionRiegoSerializer, SugerenciaSerializer, LecturaSensorSerializer, RegistroRiegoSerializer



class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer


class ZonaRiegoViewSet(viewsets.ModelViewSet):
    queryset = ZonaRiego.objects.all()
    serializer_class = ZonaRiegoSerializer


class NodoViewSet(viewsets.ModelViewSet):
    queryset = Nodo.objects.all()
    serializer_class = NodoSerializer


class SensorViewSet(viewsets.ModelViewSet):
    queryset = Sensor.objects.all()
    serializer_class = SensorSerializer


class RegadorViewSet(viewsets.ModelViewSet):
    queryset = Regador.objects.all()
    serializer_class = RegadorSerializer


class ConfiguracionRiegoViewSet(viewsets.ModelViewSet):
    queryset = ConfiguracionRiego.objects.all()
    serializer_class = ConfiguracionRiegoSerializer


class SugerenciaViewSet(viewsets.ModelViewSet):
    queryset = Sugerencia.objects.all()
    serializer_class = SugerenciaSerializer


class LecturaSensorViewSet(viewsets.ModelViewSet):
    queryset = LecturaSensor.objects.all()
    serializer_class = LecturaSensorSerializer


class RegistroRiegoViewSet(viewsets.ModelViewSet):
    queryset = RegistroRiego.objects.all()
    serializer_class = RegistroRiegoSerializer
