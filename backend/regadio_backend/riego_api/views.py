from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import ZonaRiego, LecturaSensor, Nodo, Sensor
from .serializers import ZonaRiegoSerializer, LecturaSensorSerializer, NodoSerializer, SensorSerializer
from .repository import DataRepository
import os
from django.http import JsonResponse

IS_TEST_MODE = os.getenv("MODO_TEST", "false").lower() == "true"

def return_fake_or_real(model_class, serializer_class, json_key):
    if IS_TEST_MODE:
        with open("fakedata.json") as f:
            data = json.load(f)
        return JsonResponse(data[json_key], safe=False)
    
    objetos = DataRepository.get_all(model_class)
    serializer = serializer_class(objetos, many=True)
    return Response(serializer.data)

def get_fake_by_id(json_key, id):
    with open("fakedata.json") as f:
        data = json.load(f)
    for obj in data[json_key]:
        if obj["id"] == int(id):
            return obj
    return None


# @api_view(['GET'])
# def lista_zonas(request):
#     """Obtener todas las zonas de riego"""
#     zonas = DataRepository.get_all(ZonaRiego)
#     serializer = ZonaRiegoSerializer(zonas, many=True)
#     return Response(serializer.data)
@api_view(['GET'])
def lista_zonas(request):
    return return_fake_or_real(ZonaRiego, ZonaRiegoSerializer, "zonas")

@api_view(['GET'])
def detalle_zona(request, zona_id):
    if IS_TEST_MODE:
        zona = get_fake_by_id("zonas", zona_id)
        if not zona:
            return JsonResponse({"error": "Zona no encontrada"}, status=404)
        return JsonResponse(zona, safe=False)

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
    """Obtener todas las lecturas de sensores para una zona específica"""
    try:
        # Verificar que la zona existe
        zona = DataRepository.get_by_id(ZonaRiego, zona_id)
        if not zona:
            raise ZonaRiego.DoesNotExist
        
        # Obtener lecturas donde zona_id coincide
        lecturas = DataRepository.filter(LecturaSensor, zona_id=zona)
        serializer = LecturaSensorSerializer(lecturas, many=True)
        return Response(serializer.data)
    except ZonaRiego.DoesNotExist:
        return Response({"error": "Zona no encontrada"}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def nodos_por_zona(request, zona_id):
    """Obtener todos los nodos para una zona específica"""
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
    """Obtener todos los sensores para un nodo específico"""
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
    """Obtener todas las lecturas para un sensor específico"""
    try:
        sensor = DataRepository.get_by_id(Sensor, sensor_id)
        if not sensor:
            raise Sensor.DoesNotExist
        lecturas = DataRepository.filter(LecturaSensor, sensor_id=sensor)
        serializer = LecturaSensorSerializer(lecturas, many=True)
        return Response(serializer.data)
    except Sensor.DoesNotExist:
        return Response({"error": "Sensor no encontrado"}, status=status.HTTP_404_NOT_FOUND)