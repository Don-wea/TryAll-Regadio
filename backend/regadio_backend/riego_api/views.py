from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status, viewsets
from .serializers import ZonaRiegoSerializer, LecturaSensorSerializer, NodoSerializer, SensorSerializer, HumedadSerializer, TemperaturaSerializer, FlujoSerializer
from .repository import DataRepository
from rest_framework.decorators import parser_classes
from rest_framework.parsers import JSONParser
import os
import json
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from datetime import datetime, timezone
import google.generativeai as genai
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import requests
from pymongo import MongoClient

from rest_framework_mongoengine import viewsets as mongo_viewsets
from .models import (
    Usuario, 
    ZonaRiego, 
    Nodo, 
    Sensor, 
    Regador, 
    ConfiguracionRiego, 
    Sugerencia, 
    LecturaSensor, 
    RegistroRiego, 
    Flujo, 
    Temperatura,
    Humedad
)
from .serializers import (
    ZonaRiegoSerializer, 
    NodoSerializer, 
    SensorSerializer, 
    RegadorSerializer, 
    ConfiguracionRiegoSerializer, 
    SugerenciaSerializer, 
    LecturaSensorSerializer, 
    RegistroRiegoSerializer
    )

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from .serializers import (
    UsuarioSerializer, 
    UsuarioRegisterSerializer, 
    UsuarioLoginSerializer
)
from .utils import hash_password, check_password
from mongoengine.errors import NotUniqueError, DoesNotExist
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

# JWT
import jwt
from django.conf import settings
from datetime import datetime, timedelta
#base de datos 
client = MongoClient("mongodb://localhost:27017/")
db = client['regadio_db']
#AI 
def chat_with_gemini(request):
    if request.method == 'POST':
        try:
            body = json.loads(request.body)
            prompt = body.get('message', '')
            if not prompt:
                return JsonResponse({'error': 'No message provided'}, status=400)

            # Usa tu API key aquí:
            api_key = "AIzaSyBABrw0-QDkG85bEOGux8JirHrpEEeg-Cg"
            endpoint = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={api_key}"
            headers = {'Content-Type': 'application/json'}
            data = {
                "contents": [
                    {
                        "parts": [
                            {
                                "text": prompt
                            }
                        ]
                    }
                ]
            }

            resp = requests.post(endpoint, headers=headers, json=data)
            print("[DEBUG] Gemini API resp:", resp.status_code, resp.text)  # Para depurar

            if resp.status_code == 200:
                response_json = resp.json()
                try:
                    answer = response_json['candidates'][0]['content']['parts'][0]['text']
                except Exception:
                    answer = "[Sin respuesta de Gemini]"
                return JsonResponse({'response': answer})
            else:
                return JsonResponse({'error': 'Gemini API error', 'details': resp.text}, status=500)

        except Exception as e:
            import traceback
            print("[EXCEPTION]", e)
            traceback.print_exc()
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Only POST method allowed'}, status=405)



class UsuarioRegister(APIView):
    @swagger_auto_schema(request_body=UsuarioRegisterSerializer)
    def post(self, request):
        serializer = UsuarioRegisterSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=400)
        data = serializer.validated_data
        try:
            usuario = Usuario(
                nombre_usuario=data['nombre_usuario'],
                nombre=data['nombre'],
                email=data['email'],
                password_hash=hash_password(data['password']),
                rol=data.get('rol', 'usuario'),
                fecha_registro=timezone.now()
            )
            usuario.save()
            res = UsuarioSerializer(usuario)
            return Response(res.data, status=201)
        except NotUniqueError:
            return Response({'error': 'El email o nombre de usuario ya está registrado.'}, status=400)
        except Exception as e:
            return Response({'error': str(e)}, status=400)

class UsuarioLogin(APIView):
    @swagger_auto_schema(request_body=UsuarioLoginSerializer)
    def post(self, request):
        serializer = UsuarioLoginSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=400)
        email = serializer.validated_data.get('email')
        password = serializer.validated_data.get('password')
        try:
            usuario = Usuario.objects.get(email=email)
            if not check_password(password, usuario.password_hash):
                return Response({'error': 'Credenciales inválidas'}, status=400)
            
            # Genera el JWT manualmente con PyJWT
            payload = {
                'user_id': str(usuario.id),
                'email': usuario.email,
                'rol': usuario.rol,
                'exp': datetime.utcnow() + timedelta(hours=1)
            }
            access = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')

            return Response({
                'access': access,
                'user': UsuarioSerializer(usuario).data
            })
        except DoesNotExist:
            return Response({'error': 'Credenciales inválidas'}, status=400)

class UsuarioList(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        usuarios = Usuario.objects.all()
        res = UsuarioSerializer(usuarios, many=True)
        return Response(res.data)

    @swagger_auto_schema(request_body=UsuarioRegisterSerializer)
    def post(self, request):
        serializer = UsuarioRegisterSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=400)
        data = serializer.validated_data
        try:
            usuario = Usuario(
                nombre_usuario=data['nombre_usuario'],
                nombre=data['nombre'],
                email=data['email'],
                password_hash=hash_password(data['password']),
                rol=data.get('rol', 'usuario'),
                fecha_registro=timezone.now()
            )
            usuario.save()
            return Response(UsuarioSerializer(usuario).data, status=201)
        except NotUniqueError:
            return Response({'error': 'El email o nombre de usuario ya está registrado.'}, status=400)

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


class UsuarioDetail(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, usuario_id):
        try:
            usuario = Usuario.objects.get(id=usuario_id)
            return Response(UsuarioSerializer(usuario).data)
        except DoesNotExist:
            return Response({'error': 'No encontrado'}, status=404)

    @swagger_auto_schema(request_body=UsuarioRegisterSerializer)
    def put(self, request, usuario_id):
        try:
            usuario = Usuario.objects.get(id=usuario_id)
            data = request.data
            if 'email' in data and data['email'] != usuario.email:
                if Usuario.objects(email=data['email']).first():
                    return Response({'error': 'El email ya está registrado.'}, status=400)
            for field in ['nombre_usuario', 'nombre', 'email', 'rol']:
                if field in data:
                    setattr(usuario, field, data[field])
            if 'password' in data:
                usuario.password_hash = hash_password(data['password'])
            usuario.save()
            return Response(UsuarioSerializer(usuario).data)
        except DoesNotExist:
            return Response({'error': 'No encontrado'}, status=404)
        except NotUniqueError:
            return Response({'error': 'El email o nombre de usuario ya está registrado.'}, status=400)

    def delete(self, request, usuario_id):
        try:
            usuario = Usuario.objects.get(id=usuario_id)
            usuario.delete()
            return Response({'success': True})
        except DoesNotExist:
            return Response({'error': 'No encontrado'}, status=404)


IS_TEST_MODE = os.getenv("MODO_TEST", "false").lower() in ("true", "1", "yes")
print("[DEBUG] MODO_TEST:", IS_TEST_MODE)

def load_fake_data():
    with open("fakedata.json", encoding="utf-8") as f:
        return json.load(f)

def get_fake_by_id(json_key, id):
    data = load_fake_data()
    for obj in data[json_key]:
        if str(obj.get("id")) == str(id):
            return obj
    return None

class UsuarioViewSet(viewsets.ViewSet):
    """
    ViewSet para acceder a los usuarios, usando DataRepository.
    """

    def list(self, request):
        if IS_TEST_MODE:
            data = load_fake_data()
            return Response(data.get("usuarios", []))  # Devuelve directamente la lista de usuarios fake

        usuarios = DataRepository.get_all(Usuario)
        serializer = UsuarioSerializer(usuarios, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        if IS_TEST_MODE:
            data = load_fake_data()
            usuario = None
            for u in data.get("usuarios", []):
                if str(u.get("id")) == str(pk):
                    usuario = u
                    break
            if usuario is None:
                return Response({"detail": "Usuario no encontrado"}, status=status.HTTP_404_NOT_FOUND)
            return Response(usuario)  # Devuelve el usuario fake directo

        usuario = DataRepository.get_by_id(Usuario, pk)
        if usuario is None:
            return Response({"detail": "Usuario no encontrado"}, status=status.HTTP_404_NOT_FOUND)
        serializer = UsuarioSerializer(usuario)
        return Response(serializer.data)

@api_view(['POST'])
def fake_token_obtain_pair(request):
    if not IS_TEST_MODE:
        return Response({"error": "Solo disponible en modo test"}, status=400)
    username = request.data.get("username")
    password = request.data.get("password")
    data = load_fake_data()
    usuario = next((u for u in data.get("usuarios", []) if u["nombre_usuario"] == username), None)
    if usuario is None:
        return Response({"detail": "Usuario no encontrado"}, status=401)
    if password != "test":
        return Response({"detail": "Contraseña incorrecta"}, status=401)
    
    # Crear un token manualmente
    refresh = RefreshToken()
    refresh['user_id'] = usuario['id']
    refresh['username'] = usuario['nombre_usuario']
    refresh.set_exp(lifetime=datetime.timedelta(days=7))  # refresh dura 7 días

    access = refresh.access_token
    access['user_id'] = usuario['id']
    access['username'] = usuario['nombre_usuario']
    access.set_exp(lifetime=datetime.timedelta(minutes=30))  # access dura 30 min

    return Response({
        "refresh": str(refresh),
        "access": str(access),
    })

@api_view(['GET'])
def lista_zonas(request):
    if IS_TEST_MODE:
        data = load_fake_data()
        return Response(data["zonas_riego"])
    
    objetos = DataRepository.get_all(ZonaRiego)
    serializer = ZonaRiegoSerializer(objetos, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def detalle_zona(request, zona_id):
    if IS_TEST_MODE:
        zona = get_fake_by_id("zonas_riego", zona_id)
        if not zona:
            return Response({"error": "Zona no encontrada"}, status=404)
        return Response(zona)

    try:
        zona = DataRepository.get_by_id(ZonaRiego, zona_id)
        if not zona:
            raise ZonaRiego.DoesNotExist
        serializer = ZonaRiegoSerializer(zona)
        return Response(serializer.data)
    except ZonaRiego.DoesNotExist:
        return Response({"error": "Zona no encontrada"}, status=404)

@api_view(['GET'])
def lecturas_por_zona(request, zona_id):
    if IS_TEST_MODE:
        data = load_fake_data()
        zona = get_fake_by_id("zonas_riego", zona_id)
        if not zona:
            return Response({"error": "Zona no encontrada"}, status=404)
        nombre_zona = zona["nombre"]
        lecturas = [l for l in data["lecturas_sensor"] if l["zona_id"] == nombre_zona]
        return Response(lecturas)

    try:
        zona = DataRepository.get_by_id(ZonaRiego, zona_id)
        if not zona:
            raise ZonaRiego.DoesNotExist
        lecturas = DataRepository.filter(LecturaSensor, zona_id=zona)
        serializer = LecturaSensorSerializer(lecturas, many=True)
        return Response(serializer.data)
    except ZonaRiego.DoesNotExist:
        return Response({"error": "Zona no encontrada"}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
def nodos_por_zona(request, zona_id):
    if IS_TEST_MODE:
        data = load_fake_data()
        zona = get_fake_by_id("zonas_riego", zona_id)
        if not zona:
            return Response({"error": "Zona no encontrada"}, status=404)
        nombre_zona = zona["nombre"]
        nodos = [n for n in data["nodos"] if n["zona_id"] == nombre_zona]
        return Response(nodos)

    try:
        zona = DataRepository.get_by_id(ZonaRiego, zona_id)
        if not zona:
            raise ZonaRiego.DoesNotExist
        nodos = DataRepository.filter(Nodo, zona_id=zona)
        serializer = NodoSerializer(nodos, many=True)
        return Response(serializer.data)
    except ZonaRiego.DoesNotExist:
        return Response({"error": "Zona no encontrada"}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
def sensores_por_nodo(request, nodo_id):
    if IS_TEST_MODE:
        data = load_fake_data()
        nodo = get_fake_by_id("nodos", nodo_id)
        if not nodo:
            return Response({"error": "Nodo no encontrado"}, status=404)
        nombre_nodo = nodo["nombre"]
        sensores = [s for s in data["sensores"] if s["nodo_id"] == nombre_nodo]
        return Response(sensores)

    try:
        nodo = DataRepository.get_by_id(Nodo, nodo_id)
        if not nodo:
            raise Nodo.DoesNotExist
        sensores = DataRepository.filter(Sensor, nodo_id=nodo)
        serializer = SensorSerializer(sensores, many=True)
        return Response(serializer.data)
    except Nodo.DoesNotExist:
        return Response({"error": "Nodo no encontrado"}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
def lecturas_por_sensor(request, sensor_id):
    if IS_TEST_MODE:
        data = load_fake_data()
        sensor = get_fake_by_id("sensores", sensor_id)
        if not sensor:
            return Response({"error": "Sensor no encontrado"}, status=404)
        tipo_sensor = sensor["tipo"]
        lecturas = [l for l in data["lecturas_sensor"] if l["sensor_id"] == tipo_sensor]
        return Response(lecturas)

    try:
        sensor = DataRepository.get_by_id(Sensor, sensor_id)
        if not sensor:
            raise Sensor.DoesNotExist
        lecturas = DataRepository.filter(LecturaSensor, sensor_id=sensor)
        serializer = LecturaSensorSerializer(lecturas, many=True)
        return Response(serializer.data)
    except Sensor.DoesNotExist:
        return Response({"error": "Sensor no encontrado"}, status=status.HTTP_404_NOT_FOUND)


ultimos_humedad = []  # Lista temporal mientras no uses MongoDB
ultimos_temperatura = []
ultimos_flujo = []

ultimo_id = ""

@api_view(['POST'])
def registrar_datos(request):
    global ultimo_id  # Declarar que vamos a usar la variable global

    # Obtener datos del cuerpo de la solicitud
    humedad = request.data.get("humedad", 0)
    temperatura = request.data.get("temperatura", 0)
    flujo = request.data.get("flujo", 0)
    ultimo_id = request.data.get("nodo_id", "")  # Asignar el sensor_id a la variable global

    # Validar los datos (opcional)
    if not isinstance(humedad, (int, float)) or not isinstance(temperatura, (int, float)) or not isinstance(flujo, (int, float)):
        return Response({"error": "Datos de humedad, temperatura o flujo inválidos"}, status=status.HTTP_400_BAD_REQUEST)


    ultimos_humedad.append(humedad)
    ultimos_temperatura.append(temperatura)
    ultimos_flujo.append(flujo)

    if len(ultimos_humedad) > 20:
        ultimos_humedad.pop(0)  # Guarda solo los últimos 20 valores
    if len(ultimos_temperatura) > 20:
        ultimos_temperatura.pop(0)
    if len(ultimos_flujo) > 20:
        ultimos_flujo.pop(0)

    return Response({"mensaje": "Datos recibido"}, status=200)

cantidad_flujo = 0

@api_view(['POST'])
def recibir_cantidad_flujo(request):
    global cantidad_flujo
    
    # Obtener cantidad_flujo del query parameter
    nueva_cantidad = request.query_params.get('cantidad_flujo')
    
    if nueva_cantidad is None:
        return Response(
            {"error": "Se requiere el parámetro 'cantidad_flujo'"}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    try:
        # Convertir a float
        nueva_cantidad = float(nueva_cantidad)
    except ValueError:
        return Response(
            {"error": "Cantidad de flujo debe ser un número"}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Actualizar la variable global
    cantidad_flujo = nueva_cantidad
    
    return Response({
        "mensaje": "Cantidad de flujo actualizada correctamente",
        "cantidad_flujo": cantidad_flujo
    }, status=status.HTTP_200_OK)
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.parsers import JSONParser

@swagger_auto_schema(
    method='post',
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'cantidad_flujo': openapi.Schema(type=openapi.TYPE_NUMBER, description='Cantidad de flujo objetivo (litros)')
        },
        required=['cantidad_flujo']
    ),
    responses={201: openapi.Response('Flujo registrado OK')}
)
@api_view(['POST'])
@parser_classes([JSONParser])
def guardar_flujo_objetivo(request):
    """
    Guarda el flujo objetivo en la colección 'registros_riego'
    POST /api/enviar_flujoabd/
    Body: { "cantidad_flujo": 123 }
    """
    cantidad = request.data.get('cantidad_flujo')
    if cantidad is None:
        return Response({"error": "Falta 'cantidad_flujo' en el body"}, status=status.HTTP_400_BAD_REQUEST)
    try:
        cantidad = float(cantidad)
    except Exception:
        return Response({"error": "Debe ser numérico"}, status=status.HTTP_400_BAD_REQUEST)
    registro = {
        "cantidad_agua_litros": cantidad,
        "fecha_hora_inicio": datetime.utcnow()
    }
    db.registros_riego.insert_one(registro)
    return Response({"mensaje": "Flujo objetivo guardado correctamente", "cantidad_agua_litros": cantidad}, status=status.HTTP_201_CREATED)

flujo_actual = 1
@api_view(['POST'])
def obtener_flujo_actual(request):
    global flujo_actual
    flujo_actual = request.query_params.get('flujo_actual')
    return Response({"flujo_actual": flujo_actual})

@api_view(['GET'])
def retornar_flujo_actual(request):
    return Response({"flujo_actual": flujo_actual})

@api_view(['GET'])
def enviar_cantidad_flujo(request):
    return Response({"cantidad_flujo": cantidad_flujo})  # Devuelve la cantidad de flujo como un entero o un numero decimal

ultima_humedad = 0
ultima_temperatura = 0
@api_view(['POST'])
def recibir_humedad_y_temperatura(request):
    global ultima_humedad
    global ultima_temperatura
    ultima_humedad = request.query_params.get('humedad')
    ultima_temperatura = request.query_params.get('temperatura')
    return Response({"humedad": ultima_humedad, "temperatura": ultima_temperatura})

@api_view(['GET'])
def enviar_humedad_y_temperatura(request):
    global ultima_humedad
    global ultima_temperatura
    return Response({"humedad": ultima_humedad, "temperatura": ultima_temperatura})


@api_view(['POST'])
def recibir_ultimo_id(request):
    global ultimo_id
    ultimo_id = request.query_params.get('nodo_ID')
    return Response({"nodo_ID": ultimo_id})

@api_view(['GET'])
def enviar_ultimo_id(request):
    global ultimo_id
    return Response({"ultimo_id": ultimo_id})
    

@api_view(['GET'])
def obtener_humedad(request):
    return Response({"humedad": ultimos_humedad[-1] if ultimos_humedad else 0})

@api_view(['GET'])
def obtener_temperatura(request):
    return Response({"temperatura": ultimos_temperatura[-1] if ultimos_temperatura else 0})

@api_view(['GET'])
def obtener_flujo(request):
    return Response({"flujo": ultimos_flujo[-1] if ultimos_flujo else 0})


@api_view(['GET'])
def humedad_ultima(request):
    ultimo = Humedad.objects.last()
    serializer = HumedadSerializer(ultimo)
    return Response(serializer.data)

@api_view(['GET'])
def temperatura_ultima(request):
    ultimo = Temperatura.objects.last()
    serializer = TemperaturaSerializer(ultimo)
    return Response(serializer.data)

@api_view(['GET'])
def flujo_ultimo(request):
    ultimo = Flujo.objects.last()
    serializer = FlujoSerializer(ultimo)
    return Response(serializer.data)














# ----- GET DATOS HISTORICOS -----


# Registros de riego (últimos n flujos)
@api_view(['GET'])
def historicos_ultimos_flujos(request, cantidad):
    registros = RegistroRiego.objects.order_by('-fecha_hora_inicio').limit(cantidad)
    data = [
        {
            'regador_id': str(r.regador_id.id) if r.regador_id else None,
            'zona_id': str(r.zona_id.id) if r.zona_id else None,
            'cantidad_agua_litros': r.cantidad_agua_litros,
            'energia_consumida_kwh': r.energia_consumida_kwh,
            'duracion_segundos': r.duracion_segundos,
            'fecha_hora_inicio': r.fecha_hora_inicio.isoformat(),
            'fecha_hora_fin': r.fecha_hora_fin.isoformat(),
        }
        for r in registros
    ]
    return Response(data)

# Lecturas de humedad
@api_view(['GET'])
def historicos_ultimas_humedades(request, cantidad):
    registros = LecturaSensor.objects(tipo="Humedad").order_by('-fecha_hora').limit(cantidad)
    data = [
        {
            'sensor_id': str(r.sensor_id.id) if r.sensor_id else None,
            'zona_id': str(r.zona_id.id) if r.zona_id else None,
            'valor': r.valor,
            'unidad': r.unidad,
            'fecha_hora': r.fecha_hora.isoformat(),
        }
        for r in registros
    ]
    return Response(data)

# Lecturas de temperatura
@api_view(['GET'])
def historicos_ultimas_temperaturas(request, cantidad):
    registros = LecturaSensor.objects(tipo="Temperatura").order_by('-fecha_hora').limit(cantidad)
    data = [
        {
            'sensor_id': str(r.sensor_id.id) if r.sensor_id else None,
            'zona_id': str(r.zona_id.id) if r.zona_id else None,
            'valor': r.valor,
            'unidad': r.unidad,
            'fecha_hora': r.fecha_hora.isoformat(),
        }
        for r in registros
    ]
    return Response(data)
@swagger_auto_schema(
    method='post',
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'valor': openapi.Schema(type=openapi.TYPE_NUMBER, description='Valor de humedad (%)')
        },
        required=['valor']
    ),
    responses={201: openapi.Response('Humedad registrada OK')}
)
@api_view(['POST'])
def guardar_humedad(request):
    try:
        valor = float(request.data.get('valor'))
    except Exception:
        return Response({"error": "valor es obligatorio y debe ser numérico"}, status=status.HTTP_400_BAD_REQUEST)
    registro = {
        "tipo": "Humedad",
        "valor": valor,
        "fecha_hora": datetime.utcnow()
    }
    db.lecturas_sensor.insert_one(registro)
    return Response({"mensaje": "Humedad guardada correctamente"}, status=status.HTTP_201_CREATED)


@swagger_auto_schema(
    method='post',
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'valor': openapi.Schema(type=openapi.TYPE_NUMBER, description='Valor de temperatura (°C)')
        },
        required=['valor']
    ),
    responses={201: openapi.Response('Temperatura registrada OK')}
)
@api_view(['POST'])
def guardar_temperatura(request):
    try:
        valor = float(request.data.get('valor'))
    except Exception:
        return Response({"error": "valor es obligatorio y debe ser numérico"}, status=status.HTTP_400_BAD_REQUEST)
    registro = {
        "tipo": "Temperatura",
        "valor": valor,
        "fecha_hora": datetime.utcnow()
    }
    db.lecturas_sensor.insert_one(registro)
    return Response({"mensaje": "Temperatura guardada correctamente"}, status=status.HTTP_201_CREATED)
