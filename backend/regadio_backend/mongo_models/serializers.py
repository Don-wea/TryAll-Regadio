# from rest_framework_mongoengine import serializers as mongo_serializers
# from rest_framework import serializers
# from .models import Usuario, ProgramacionDia, ZonaRiego, Nodo, Sensor, Regador, ConfiguracionRiego, Sugerencia, LecturaSensor, RegistroRiego



# class UsuarioSerializer(serializers.Serializer):
#     id = serializers.CharField(read_only=True)
#     nombre_usuario = serializers.CharField()
#     nombre = serializers.CharField()
#     email = serializers.EmailField()
#     rol = serializers.CharField()
#     fecha_registro = serializers.DateTimeField(read_only=True)

# class UsuarioRegisterSerializer(serializers.Serializer):
#     nombre_usuario = serializers.CharField()
#     nombre = serializers.CharField()
#     email = serializers.EmailField()
#     password = serializers.CharField(write_only=True)
#     rol = serializers.CharField(required=False)

# class UsuarioLoginSerializer(serializers.Serializer):
#     email = serializers.EmailField()
#     password = serializers.CharField(write_only=True)

# # 📦 ProgramacionDia (Embedded)
# class ProgramacionDiaSerializer(mongo_serializers.DocumentSerializer):
#     class Meta:
#         model = ProgramacionDia
#         fields = '__all__'


# # 📦 ZonaRiego
# class ZonaRiegoSerializer(mongo_serializers.DocumentSerializer):
#     class Meta:
#         model = ZonaRiego
#         fields = '__all__'


# # 📦 Nodo
# class NodoSerializer(mongo_serializers.DocumentSerializer):
#     class Meta:
#         model = Nodo
#         fields = '__all__'


# # 📦 Sensor
# class SensorSerializer(mongo_serializers.DocumentSerializer):
#     class Meta:
#         model = Sensor
#         fields = '__all__'


# # 📦 Regador
# class RegadorSerializer(mongo_serializers.DocumentSerializer):
#     class Meta:
#         model = Regador
#         fields = '__all__'


# # 📦 ConfiguracionRiego
# class ConfiguracionRiegoSerializer(mongo_serializers.DocumentSerializer):
#     programacion = ProgramacionDiaSerializer()

#     class Meta:
#         model = ConfiguracionRiego
#         fields = '__all__'


# # 📦 Sugerencia
# class SugerenciaSerializer(mongo_serializers.DocumentSerializer):
#     class Meta:
#         model = Sugerencia
#         fields = '__all__'


# # 📦 LecturaSensor
# class LecturaSensorSerializer(mongo_serializers.DocumentSerializer):
#     class Meta:
#         model = LecturaSensor
#         fields = '__all__'


# # 📦 RegistroRiego
# class RegistroRiegoSerializer(mongo_serializers.DocumentSerializer):
#     class Meta:
#         model = RegistroRiego
#         fields = '__all__'
