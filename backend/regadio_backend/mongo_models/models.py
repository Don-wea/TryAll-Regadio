from mongoengine import Document, EmbeddedDocument, EmbeddedDocumentField
from mongoengine import StringField, EmailField, DateTimeField, ReferenceField, FloatField
from mongoengine import IntField, BooleanField, ListField, PointField, EnumField
from mongoengine import ObjectIdField
import datetime 
import enum


# 📦 Usuario
class Usuario(Document):
    nombre_usuario = StringField(required=True, unique=True)
    nombre = StringField(required=True)
    email = EmailField(required=True, unique=True)
    password_hash = StringField(required=True)
    rol = StringField(required=True)
    fecha_registro = DateTimeField(default=lambda: datetime.datetime.now(datetime.timezone.utc))
    meta = {
        'collection': 'setup'
    }

    def __str__(self):
        return f"{self.nombre_usuario} ({self.nombre})"

# 📦 ProgramacionDia (Embedded)
class ProgramacionDia(EmbeddedDocument):
    dia = StringField(required=True)
    hora_inicio = StringField(required=True)
    duracion_minutos = IntField(required=True)
    humedad_objetivo = FloatField(required=True)
    ph_minimo = FloatField(required=True)
    ph_maximo = FloatField(required=True)
    temperatura_maxima = FloatField(required=True)


# 📦 ZonaRiego
class ZonaRiego(Document):
    usuario = ReferenceField(Usuario, required=False)
    nombre = StringField(required=True)
    ubicacion = StringField()  # Could use a GeoJSON or complex object if needed
    fecha_creacion = DateTimeField(default=lambda: datetime.datetime.now(datetime.timezone.utc))


# 📦 Nodo
class Nodo(Document):
    zona = ReferenceField(ZonaRiego, required=True)
    nombre = StringField(required=True)
    descripcion = StringField()
    coordenadas = PointField(required=True)


# 📦 Sensor
class Sensor(Document):
    nodo = ReferenceField(Nodo, required=True)
    tipo = StringField(required=True)
    modelo = StringField(required=True)
    descripcion = StringField()


# 📦 Regador
class Regador(Document):
    nodo = ReferenceField(Nodo, required=True)
    modelo = StringField(required=True)
    descripcion = StringField()


# 📦 ConfiguracionRiego
class ConfiguracionRiego(Document):
    zona = ReferenceField(ZonaRiego, required=True)
    programacion = EmbeddedDocumentField(ProgramacionDia)


# 📦 Sugerencia
class Sugerencia(Document):
    IMPACTO_CHOICES = ('bajo', 'medio', 'alto')
    zona = ReferenceField(ZonaRiego, required=True)
    fecha = DateTimeField(default=lambda: datetime.datetime.now(datetime.timezone.utc))
    mensaje = StringField(required=True)
    impacto = StringField(choices=IMPACTO_CHOICES)


# 📦 LecturaSensor
class LecturaSensor(Document):
    sensor = ReferenceField(Sensor, required=True)
    nodo = ReferenceField(Nodo, required=True)
    zona = ReferenceField(ZonaRiego, required=True)
    tipo = StringField(required=True)
    valor = FloatField(required=True)
    unidad = StringField(required=True)
    fecha_hora = DateTimeField(default=lambda: datetime.datetime.now(datetime.timezone.utc))


# 📦 RegistroRiego
class RegistroRiego(Document):
    regador = ReferenceField(Regador, required=True)
    nodo = ReferenceField(Nodo, required=True)
    zona = ReferenceField(ZonaRiego, required=True)
    cantidad_agua_litros = FloatField(required=True)
    energia_consumida_kwh = FloatField(required=True)
    duracion_segundos = IntField(required=True)
    fecha_hora_inicio = DateTimeField(required=True)
    fecha_hora_fin = DateTimeField(required=True)
