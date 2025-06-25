from rest_framework import serializers
from rest_framework_mongoengine import serializers as mongo_serializers
from .models import (
    Usuario, 
    ZonaRiego, 
    LecturaSensor, 
    Nodo, 
    Sensor, 
    Humedad, 
    Temperatura, 
    Flujo, 
    ID,
    Regador,
    ConfiguracionRiego,
    ProgramacionDia,
    Sugerencia,
    RegistroRiego,
    )
# login del gudmar
class UsuarioSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)
    nombre_usuario = serializers.CharField()
    nombre = serializers.CharField()
    email = serializers.EmailField()
    rol = serializers.CharField()
    fecha_registro = serializers.DateTimeField(read_only=True)

class UsuarioRegisterSerializer(serializers.Serializer):
    nombre_usuario = serializers.CharField()
    nombre = serializers.CharField()
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    rol = serializers.CharField(required=False)

class UsuarioLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)


class ZonaRiegoSerializer(mongo_serializers.DocumentSerializer):
    class Meta:
        model = ZonaRiego
        fields = '__all__'

class RegadorSerializer(mongo_serializers.DocumentSerializer):
    class Meta:
        model = Regador
        fields = '__all__'

class NodoSerializer(mongo_serializers.DocumentSerializer):
    class Meta:
        model = Nodo
        fields = '__all__'


class SensorSerializer(mongo_serializers.DocumentSerializer):
    class Meta:
        model = Sensor
        fields = '__all__'


class LecturaSensorSerializer(mongo_serializers.DocumentSerializer):
    class Meta:
        model = LecturaSensor
        fields = '__all__'


class HumedadSerializer(mongo_serializers.DocumentSerializer):
    class Meta:
        model = Humedad
        fields = '__all__'

class TemperaturaSerializer(mongo_serializers.DocumentSerializer):
    class Meta:
        model = Temperatura
        fields = '__all__'

class FlujoSerializer(mongo_serializers.DocumentSerializer):
    class Meta:
        model = Flujo
        fields = '__all__'

class IdSerializer(mongo_serializers.DocumentSerializer):
    class Meta:
        model = ID
        fields = '__all__'
        



# Serializer directo ligado al modelo mongoengine para leer/editar completo
class UsuarioDocumentSerializer(mongo_serializers.DocumentSerializer):
    class Meta:
        model = Usuario
        fields = '__all__'

class ProgramacionDiaSerializer(mongo_serializers.DocumentSerializer):
    class Meta:
        model = ProgramacionDia
        fields = '__all__'

class ConfiguracionRiegoSerializer(mongo_serializers.DocumentSerializer):
    programacion = ProgramacionDiaSerializer()

    class Meta:
        model = ConfiguracionRiego
        fields = '__all__'

class SugerenciaSerializer(mongo_serializers.DocumentSerializer):
    class Meta:
        model = Sugerencia
        fields = '__all__'

class RegistroRiegoSerializer(mongo_serializers.DocumentSerializer):
    class Meta:
        model = RegistroRiego
        fields = '__all__'
