from mongoengine import Document, EmbeddedDocument, EmbeddedDocumentField
from mongoengine import StringField, EmailField, DateTimeField, ReferenceField, FloatField
from mongoengine import IntField, BooleanField, ListField, PointField, EnumField
from mongoengine import ObjectIdField
from datetime import datetime, timezone
import enum

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
    nombre = StringField(required=True, max_length=100)
    ubicacion = StringField()
    fecha_creacion = DateTimeField(default=lambda: datetime.now(timezone.utc))
    usuario = ReferenceField(Usuario, required=True)

    meta = {
        'collection': 'zonas_riego'
    }

    def __str__(self):
        return self.nombre

class Nodo(Document):
    _id = ObjectIdField()
    zona_id = ReferenceField(ZonaRiego, required=True)
    nombre = StringField(required=True, max_length=100)
    descripcion = StringField()
    coordenadas = PointField()

    meta = {
        'collection': 'nodos'
    }

    def __str__(self):
        return f"{self.nombre}"

class Sensor(Document):
    _id = ObjectIdField()
    nodo_id = ReferenceField(Nodo, required=True)
    tipo = StringField(required=True, choices=TipoSensor)
    modelo = StringField()
    descripcion = StringField()

    meta = {
        'collection': 'sensores'
    }

    def __str__(self):
        return f"{self.tipo} en {self.nodo_id.nombre}"

class LecturaSensor(Document):
    _id = ObjectIdField()
    sensor_id = ReferenceField(Sensor, required=True)
    nodo_id = ReferenceField(Nodo, required=True)
    zona_id = ReferenceField(ZonaRiego, required=True)
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
    _id = ObjectIdField()
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
    _id = ObjectIdField()
    zona_id = ReferenceField(ZonaRiego, required=True, unique=True)
    programacion = ListField(EmbeddedDocumentField(ProgramacionDia))

    meta = {
        'collection': 'configuraciones_riego'
    }

    def __str__(self):
        return f"Configuración para {self.zona_id.nombre}"

class Regador(Document):
    _id = ObjectIdField()
    nodo_id = ReferenceField(Nodo, required=True)
    modelo = StringField()
    descripcion = StringField()

    meta = {
        'collection': 'regadores'
    }

    def __str__(self):
        return f"Regador en {self.nodo_id.nombre}"

class RegistroRiego(Document):
    _id = ObjectIdField()
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