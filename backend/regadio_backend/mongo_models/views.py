# from rest_framework_mongoengine import viewsets
# from .models import Usuario, ZonaRiego, Nodo, Sensor, Regador, ConfiguracionRiego, Sugerencia, LecturaSensor, RegistroRiego

# from .serializers import (
#     ZonaRiegoSerializer, 
#     NodoSerializer, 
#     SensorSerializer, 
#     RegadorSerializer, 
#     ConfiguracionRiegoSerializer, 
#     SugerenciaSerializer, 
#     LecturaSensorSerializer, 
#     RegistroRiegoSerializer
#     )

# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework.permissions import IsAuthenticated
# from django.utils import timezone
# from .serializers import (
#     UsuarioSerializer, 
#     UsuarioRegisterSerializer, 
#     UsuarioLoginSerializer
# )
# from .utils import hash_password, check_password
# from mongoengine.errors import NotUniqueError, DoesNotExist
# from drf_yasg.utils import swagger_auto_schema

# # JWT
# import jwt
# from django.conf import settings
# from datetime import datetime, timedelta

# class UsuarioRegister(APIView):
#     @swagger_auto_schema(request_body=UsuarioRegisterSerializer)
#     def post(self, request):
#         serializer = UsuarioRegisterSerializer(data=request.data)
#         if not serializer.is_valid():
#             return Response(serializer.errors, status=400)
#         data = serializer.validated_data
#         try:
#             usuario = Usuario(
#                 nombre_usuario=data['nombre_usuario'],
#                 nombre=data['nombre'],
#                 email=data['email'],
#                 password_hash=hash_password(data['password']),
#                 rol=data.get('rol', 'usuario'),
#                 fecha_registro=timezone.now()
#             )
#             usuario.save()
#             res = UsuarioSerializer(usuario)
#             return Response(res.data, status=201)
#         except NotUniqueError:
#             return Response({'error': 'El email o nombre de usuario ya está registrado.'}, status=400)
#         except Exception as e:
#             return Response({'error': str(e)}, status=400)

# class UsuarioLogin(APIView):
#     @swagger_auto_schema(request_body=UsuarioLoginSerializer)
#     def post(self, request):
#         serializer = UsuarioLoginSerializer(data=request.data)
#         if not serializer.is_valid():
#             return Response(serializer.errors, status=400)
#         email = serializer.validated_data.get('email')
#         password = serializer.validated_data.get('password')
#         try:
#             usuario = Usuario.objects.get(email=email)
#             if not check_password(password, usuario.password_hash):
#                 return Response({'error': 'Credenciales inválidas'}, status=400)
            
#             # Genera el JWT manualmente con PyJWT
#             payload = {
#                 'user_id': str(usuario.id),
#                 'email': usuario.email,
#                 'rol': usuario.rol,
#                 'exp': datetime.utcnow() + timedelta(hours=1)
#             }
#             access = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')

#             return Response({
#                 'access': access,
#                 'user': UsuarioSerializer(usuario).data
#             })
#         except DoesNotExist:
#             return Response({'error': 'Credenciales inválidas'}, status=400)

# class UsuarioList(APIView):
#     permission_classes = [IsAuthenticated]

#     def get(self, request):
#         usuarios = Usuario.objects.all()
#         res = UsuarioSerializer(usuarios, many=True)
#         return Response(res.data)

#     @swagger_auto_schema(request_body=UsuarioRegisterSerializer)
#     def post(self, request):
#         serializer = UsuarioRegisterSerializer(data=request.data)
#         if not serializer.is_valid():
#             return Response(serializer.errors, status=400)
#         data = serializer.validated_data
#         try:
#             usuario = Usuario(
#                 nombre_usuario=data['nombre_usuario'],
#                 nombre=data['nombre'],
#                 email=data['email'],
#                 password_hash=hash_password(data['password']),
#                 rol=data.get('rol', 'usuario'),
#                 fecha_registro=timezone.now()
#             )
#             usuario.save()
#             return Response(UsuarioSerializer(usuario).data, status=201)
#         except NotUniqueError:
#             return Response({'error': 'El email o nombre de usuario ya está registrado.'}, status=400)

# class UsuarioDetail(APIView):
#     permission_classes = [IsAuthenticated]

#     def get(self, request, usuario_id):
#         try:
#             usuario = Usuario.objects.get(id=usuario_id)
#             return Response(UsuarioSerializer(usuario).data)
#         except DoesNotExist:
#             return Response({'error': 'No encontrado'}, status=404)

#     @swagger_auto_schema(request_body=UsuarioRegisterSerializer)
#     def put(self, request, usuario_id):
#         try:
#             usuario = Usuario.objects.get(id=usuario_id)
#             data = request.data
#             if 'email' in data and data['email'] != usuario.email:
#                 if Usuario.objects(email=data['email']).first():
#                     return Response({'error': 'El email ya está registrado.'}, status=400)
#             for field in ['nombre_usuario', 'nombre', 'email', 'rol']:
#                 if field in data:
#                     setattr(usuario, field, data[field])
#             if 'password' in data:
#                 usuario.password_hash = hash_password(data['password'])
#             usuario.save()
#             return Response(UsuarioSerializer(usuario).data)
#         except DoesNotExist:
#             return Response({'error': 'No encontrado'}, status=404)
#         except NotUniqueError:
#             return Response({'error': 'El email o nombre de usuario ya está registrado.'}, status=400)

#     def delete(self, request, usuario_id):
#         try:
#             usuario = Usuario.objects.get(id=usuario_id)
#             usuario.delete()
#             return Response({'success': True})
#         except DoesNotExist:
#             return Response({'error': 'No encontrado'}, status=404)



# class ZonaRiegoViewSet(viewsets.ModelViewSet):
#     queryset = ZonaRiego.objects.all()
#     serializer_class = ZonaRiegoSerializer


# class NodoViewSet(viewsets.ModelViewSet):
#     queryset = Nodo.objects.all()
#     serializer_class = NodoSerializer


# class SensorViewSet(viewsets.ModelViewSet):
#     queryset = Sensor.objects.all()
#     serializer_class = SensorSerializer


# class RegadorViewSet(viewsets.ModelViewSet):
#     queryset = Regador.objects.all()
#     serializer_class = RegadorSerializer


# class ConfiguracionRiegoViewSet(viewsets.ModelViewSet):
#     queryset = ConfiguracionRiego.objects.all()
#     serializer_class = ConfiguracionRiegoSerializer


# class SugerenciaViewSet(viewsets.ModelViewSet):
#     queryset = Sugerencia.objects.all()
#     serializer_class = SugerenciaSerializer


# class LecturaSensorViewSet(viewsets.ModelViewSet):
#     queryset = LecturaSensor.objects.all()
#     serializer_class = LecturaSensorSerializer


# class RegistroRiegoViewSet(viewsets.ModelViewSet):
#     queryset = RegistroRiego.objects.all()
#     serializer_class = RegistroRiegoSerializer
