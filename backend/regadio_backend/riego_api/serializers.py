from rest_framework_mongoengine import serializers
from .models import ZonaRiego, LecturaSensor, Nodo, Sensor, Humedad, Temperatura, Flujo


class ZonaRiegoSerializer(serializers.DocumentSerializer):
    class Meta:
        model = ZonaRiego
        fields = '__all__'


class NodoSerializer(serializers.DocumentSerializer):
    class Meta:
        model = Nodo
        fields = '__all__'


class SensorSerializer(serializers.DocumentSerializer):
    class Meta:
        model = Sensor
        fields = '__all__'


class LecturaSensorSerializer(serializers.DocumentSerializer):
    class Meta:
        model = LecturaSensor
        fields = '__all__'


class HumedadSerializer(serializers.DocumentSerializer):
    class Meta:
        model = Humedad
        fields = '__all__'

class TemperaturaSerializer(serializers.DocumentSerializer):
    class Meta:
        model = Temperatura
        fields = '__all__'

class FlujoSerializer(serializers.DocumentSerializer):
    class Meta:
        model = Flujo
        fields = '__all__'