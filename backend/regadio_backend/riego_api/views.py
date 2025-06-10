from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import ZonaRiego, LecturaSensor, Nodo, Sensor
from .serializers import ZonaRiegoSerializer, LecturaSensorSerializer, NodoSerializer, SensorSerializer


@api_view(['GET'])
def lista_zonas(request):
    """Obtener todas las zonas de riego"""
    zonas = ZonaRiego.objects.all()
    serializer = ZonaRiegoSerializer(zonas, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def detalle_zona(request, zona_id):
    """Obtener una zona específica por ID"""
    try:
        zona = ZonaRiego.objects.get(id=zona_id)
        serializer = ZonaRiegoSerializer(zona)
        return Response(serializer.data)
    except ZonaRiego.DoesNotExist:
        return Response({"error": "Zona no encontrada"}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def lecturas_por_zona(request, zona_id):
    """Obtener todas las lecturas de sensores para una zona específica"""
    try:
        # Verificar que la zona existe
        zona = ZonaRiego.objects.get(id=zona_id)
        
        # Obtener lecturas donde zona_id coincide
        lecturas = LecturaSensor.objects.filter(zona_id=zona)
        serializer = LecturaSensorSerializer(lecturas, many=True)
        return Response(serializer.data)
    except ZonaRiego.DoesNotExist:
        return Response({"error": "Zona no encontrada"}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def nodos_por_zona(request, zona_id):
    """Obtener todos los nodos para una zona específica"""
    try:
        zona = ZonaRiego.objects.get(id=zona_id)
        nodos = Nodo.objects.filter(zona_id=zona)
        serializer = NodoSerializer(nodos, many=True)
        return Response(serializer.data)
    except ZonaRiego.DoesNotExist:
        return Response({"error": "Zona no encontrada"}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def sensores_por_nodo(request, nodo_id):
    """Obtener todos los sensores para un nodo específico"""
    try:
        nodo = Nodo.objects.get(id=nodo_id)
        sensores = Sensor.objects.filter(nodo_id=nodo)
        serializer = SensorSerializer(sensores, many=True)
        return Response(serializer.data)
    except Nodo.DoesNotExist:
        return Response({"error": "Nodo no encontrado"}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def lecturas_por_sensor(request, sensor_id):
    """Obtener todas las lecturas para un sensor específico"""
    try:
        sensor = Sensor.objects.get(id=sensor_id)
        lecturas = LecturaSensor.objects.filter(sensor_id=sensor)
        serializer = LecturaSensorSerializer(lecturas, many=True)
        return Response(serializer.data)
    except Sensor.DoesNotExist:
        return Response({"error": "Sensor no encontrado"}, status=status.HTTP_404_NOT_FOUND)