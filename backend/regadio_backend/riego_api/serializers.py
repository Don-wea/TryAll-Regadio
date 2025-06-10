from rest_framework_mongoengine import serializers
from .models import ZonaRiego, LecturaSensor, Nodo, Sensor


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