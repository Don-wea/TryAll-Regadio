# from rest_framework import serializers

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
