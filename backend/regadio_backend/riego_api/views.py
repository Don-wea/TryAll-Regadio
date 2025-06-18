from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import ZonaRiego, LecturaSensor, Nodo, Sensor, Humedad, Temperatura, Flujo
from .serializers import ZonaRiegoSerializer, LecturaSensorSerializer, NodoSerializer, SensorSerializer, HumedadSerializer, TemperaturaSerializer, FlujoSerializer
from .repository import DataRepository
import os
import json

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

@api_view(['POST'])
def registrar_datos(request):
    humedad = request.data.get("humedad", 0)
    temperatura = request.data.get("temperatura", 0)
    flujo = request.data.get("flujo", 0)

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