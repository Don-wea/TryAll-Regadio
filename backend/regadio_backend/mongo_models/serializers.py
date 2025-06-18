from rest_framework_mongoengine import serializers
from .models import Usuario, ProgramacionDia, ZonaRiego, Nodo, Sensor, Regador, ConfiguracionRiego, Sugerencia, LecturaSensor, RegistroRiego


# 📦 ProgramacionDia (Embedded)
class ProgramacionDiaSerializer(serializers.EmbeddedDocumentSerializer):
    class Meta:
        model = ProgramacionDia
        fields = '__all__'


# 📦 Usuario
class UsuarioSerializer(serializers.DocumentSerializer):
    class Meta:
        model = Usuario
        fields = '__all__'


# 📦 ZonaRiego
class ZonaRiegoSerializer(serializers.DocumentSerializer):
    class Meta:
        model = ZonaRiego
        fields = '__all__'


# 📦 Nodo
class NodoSerializer(serializers.DocumentSerializer):
    class Meta:
        model = Nodo
        fields = '__all__'


# 📦 Sensor
class SensorSerializer(serializers.DocumentSerializer):
    class Meta:
        model = Sensor
        fields = '__all__'


# 📦 Regador
class RegadorSerializer(serializers.DocumentSerializer):
    class Meta:
        model = Regador
        fields = '__all__'


# 📦 ConfiguracionRiego
class ConfiguracionRiegoSerializer(serializers.DocumentSerializer):
    programacion = ProgramacionDiaSerializer()

    class Meta:
        model = ConfiguracionRiego
        fields = '__all__'


# 📦 Sugerencia
class SugerenciaSerializer(serializers.DocumentSerializer):
    class Meta:
        model = Sugerencia
        fields = '__all__'


# 📦 LecturaSensor
class LecturaSensorSerializer(serializers.DocumentSerializer):
    class Meta:
        model = LecturaSensor
        fields = '__all__'


# 📦 RegistroRiego
class RegistroRiegoSerializer(serializers.DocumentSerializer):
    class Meta:
        model = RegistroRiego
        fields = '__all__'
