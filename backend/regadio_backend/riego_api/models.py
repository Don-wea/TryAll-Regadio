from mongoengine import Document, EmbeddedDocument, EmbeddedDocumentField
from mongoengine import StringField, EmailField, DateTimeField, ReferenceField, FloatField
from mongoengine import IntField, BooleanField, ListField, PointField, EnumField
from mongoengine import ObjectIdField
from datetime import datetime, timezone
from django.db import models
import enum


# Para convertir objetos MongoEngine a diccionario simple para JSON
def to_dict(doc):
    # .to_mongo() devuelve un SON (dict BSON), lo convertimos a dict normal y eliminamos _cls si existe
    d = doc.to_mongo().to_dict()
    d.pop('_cls', None)  # opcional si usas herencia
    # Convertir ObjectId a str para JSON si existe
    if '_id' in d:
        d['_id'] = str(d['_id'])
    return d

# Enumeraciones
class Impacto(enum.Enum):
    BAJO = 'bajo'
    MEDIO = 'medio'
    ALTO = 'alto'
    CRITICO = 'critico'

class TipoSensor(enum.Enum):
    HUMEDAD_SUELO = 'humedad_suelo'
    TEMPERATURA = 'temperatura'
    HUMEDAD_AMBIENTE = 'humedad_ambiente'
    LLUVIA = 'lluvia'
    LUZ = 'luz'
    VIENTO = 'viento'

class TipoRegador(enum.Enum):
    ASPERSOR = 'aspersor'
    GOTEO = 'goteo'
    NEBULIZADOR = 'nebulizador'
    MICROASPERSOR = 'microaspersor'

class DiaSemana(enum.Enum):
    LUNES = 1
    MARTES = 2
    MIERCOLES = 3
    JUEVES = 4
    VIERNES = 5
    SABADO = 6
    DOMINGO = 7

# Modelos
class Usuario(Document):
    nombre_usuario = StringField(required=True, unique=True)
    nombre = StringField(required=True)
    email = EmailField(required=True, unique=True)
    password_hash = StringField(required=True)
    rol = StringField(required=True, choices=['admin', 'usuario'], default='usuario')
    fecha_registro = DateTimeField(default=lambda: datetime.now(timezone.utc))

    meta = {
        'collection': 'usuarios'
    }

    def __str__(self):
        return f"{self.nombre_usuario} ({self.nombre})"

class ZonaRiego(Document):
    usuario_id = ReferenceField(Usuario, required=True)
    nombre = StringField(required=True, max_length=100)
    ubicacion = StringField()
    fecha_creacion = DateTimeField(default=lambda: datetime.now(timezone.utc))
    

    meta = {
        'collection': 'zonas_riego'
    }

    def __str__(self):
        return f"ZonaRiego: {self.nombre} (Usuario: {self.usuario_id.nombre_usuario if self.usuario_id else 'N/A'})"

    def to_dict(self):
        d = to_dict(self)
        # Agregar usuario como dict o solo su id
        if self.usuario_id:
            d['usuario'] = str(self.usuario_id.id)
        return d



class Nodo(Document):
    zona_id = ReferenceField(ZonaRiego, required=True)
    nombre = StringField(required=True, max_length=100)
    descripcion = StringField()
    coordenadas = PointField()

    meta = {
        'collection': 'nodos'
    }

    def __str__(self):
        return f"Nodo: {self.nombre} (Zona: {self.zona_id.nombre})"

    def to_dict(self):
        d = to_dict(self)
        d['zona'] = str(self.zona_id.id)
        return d

class Sensor(Document):
    nodo_id = ReferenceField(Nodo, required=True)
    tipo = StringField(required=True)
    modelo = StringField()
    descripcion = StringField()

    meta = {
        'collection': 'sensores'
    }

    def __str__(self):
        return f"{self.tipo} en {self.nodo_id.nombre}"

class LecturaSensor(Document):
    sensor_id = ReferenceField(Sensor, required=True)
    nodo_id = ReferenceField(Nodo, required=True)
    zona_id = ReferenceField(ZonaRiego, required=True)
    tipo = StringField()
    valor = FloatField(required=True)
    unidad = StringField()
    fecha_hora = DateTimeField(default=lambda: datetime.now(timezone.utc))

    meta = {
        'collection': 'lecturas_sensor',
        'indexes': [
            {'fields': ['fecha_hora'], 'expireAfterSeconds': 7776000}  # 90 días
        ]
    }

    def __str__(self):
        return f"{self.sensor_id.tipo}: {self.valor} {self.unidad}"

class Sugerencia(Document):
    IMPACTO_CHOICES = ('bajo', 'medio', 'alto')
    zona_id = ReferenceField(ZonaRiego, required=True)
    fecha = DateTimeField(default=lambda: datetime.now(timezone.utc))
    mensaje = StringField(required=True)
    impacto = EnumField(Impacto, default=Impacto.MEDIO)

    meta = {
        'collection': 'sugerencias'
    }

    def __str__(self):
        return f"Sugerencia para {self.zona_id.nombre}: {self.impacto.value}"

class ProgramacionDia(EmbeddedDocument):
    dia = StringField(required=True, max_length=10)
    hora_inicio = StringField(required=True)
    duracion_minutos = IntField(required=True, min_value=1)
    humedad_objetivo = FloatField(min_value=0, max_value=100)
    ph_minimo = FloatField()
    ph_maximo = FloatField()
    temperatura_maxima = FloatField()

class ConfiguracionRiego(Document):
    zona_id = ReferenceField(ZonaRiego, required=True)
    programacion = EmbeddedDocumentField(ProgramacionDia)
    # programacion = ListField(EmbeddedDocumentField(ProgramacionDia))

    meta = {
        'collection': 'configuraciones_riego'
    }

    def __str__(self):
        return f"Configuración para {self.zona_id.nombre}"

class Regador(Document):
    nodo_id = ReferenceField(Nodo, required=True)
    modelo = StringField()
    descripcion = StringField()

    meta = {
        'collection': 'regadores'
    }

    def __str__(self):
        return f"Regador en {self.nodo_id.nombre}"

class RegistroRiego(Document):
    regador_id = ReferenceField(Regador, required=True)
    nodo_id = ReferenceField(Nodo, required=True)
    zona_id = ReferenceField(ZonaRiego, required=True)
    cantidad_agua_litros = FloatField(required=True)
    energia_consumida_kwh = FloatField()
    duracion_segundos = IntField(required=True)
    fecha_hora_inicio = DateTimeField(required=True)
    fecha_hora_fin = DateTimeField()

    meta = {
        'collection': 'registros_riego'
    }

    def __str__(self):
        return f"Riego en {self.zona_id.nombre} - {self.fecha_hora_inicio}"

class Humedad(Document):
    valor = FloatField(required=True)
    timestamp = DateTimeField(default=datetime.now)
    sensor_id = StringField(required=True)

class Temperatura(Document):
    valor = FloatField(required=True)
    timestamp = DateTimeField(default=datetime.now)
    sensor_id = StringField(required=True)

class Flujo(Document):
    valor = FloatField(required=True)
    timestamp = DateTimeField(default=datetime.now)
    sensor_id = StringField(required=True)

class ID(Document):
    valor = FloatField(required=True)
    timestamp = DateTimeField(default=datetime.now)
    sensor_id = StringField(required=True)