from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import ZonaRiego, LecturaSensor, Nodo, Sensor, Humedad
from .serializers import ZonaRiegoSerializer, LecturaSensorSerializer, NodoSerializer, SensorSerializer, HumedadSerializer


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


ultimos_valores = []  # Lista temporal mientras no uses MongoDB

@api_view(['POST'])
def registrar_humedad(request):
    humedad = request.data.get("humedad", 0)
    ultimos_valores.append(humedad)
    if len(ultimos_valores) > 20:
        ultimos_valores.pop(0)  # Guarda solo los últimos 20 valores
    return Response({"mensaje": "Dato recibido"}, status=200)

@api_view(['GET'])
def obtener_humedad(request):
    return Response({"humedad": ultimos_valores[-1] if ultimos_valores else 0})


@api_view(['GET'])
def humedad_ultima(request):
    ultimo = Humedad.objects.last()
    serializer = HumedadSerializer(ultimo)
    return Response(serializer.data)