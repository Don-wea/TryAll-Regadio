from rest_framework import serializers
from rest_framework_mongoengine import serializers as mongo_serializers
from .models import Usuario, ZonaRiego, LecturaSensor, Nodo, Sensor, Humedad, Temperatura, Flujo, ID


class ZonaRiegoSerializer(mongo_serializers.DocumentSerializer):
    class Meta:
        model = ZonaRiego
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
        
class UsuarioSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=100)
    email = serializers.EmailField()
    nombre = serializers.CharField(max_length=200, required=False, allow_blank=True)

    def create(self, validated_data):
        # Crear usuario en la base con mongoengine
        return Usuario(**validated_data).save()

    def update(self, instance, validated_data):
        instance.username = validated_data.get('username', instance.username)
        instance.email = validated_data.get('email', instance.email)
        instance.nombre = validated_data.get('nombre', instance.nombre)
        instance.save()
        return instance


# Serializer directo ligado al modelo mongoengine para leer/editar completo
class UsuarioDocumentSerializer(mongo_serializers.DocumentSerializer):
    class Meta:
        model = Usuario
        fields = '__all__'