from mongoengine import Document, EmbeddedDocument, EmbeddedDocumentField
from mongoengine import StringField, EmailField, DateTimeField, ReferenceField, FloatField
from mongoengine import IntField, PointField
import datetime

# Para convertir objetos MongoEngine a diccionario simple para JSON
def to_dict(doc):
    # .to_mongo() devuelve un SON (dict BSON), lo convertimos a dict normal y eliminamos _cls si existe
    d = doc.to_mongo().to_dict()
    d.pop('_cls', None)  # opcional si usas herencia
    # Convertir ObjectId a str para JSON si existe
    if '_id' in d:
        d['_id'] = str(d['_id'])
    return d


class Usuario(Document):
    nombre_usuario = StringField(required=True, unique=True)
    nombre = StringField(required=True)
    email = EmailField(required=True, unique=True)
    password_hash = StringField(required=True)
    rol = StringField #(required=True)
    fecha_registro = DateTimeField(default=lambda: datetime.datetime.now(datetime.timezone.utc))

    # meta = {
    #     'collection': 'setup'
    # }

    def __str__(self):
        return f"Usuario: {self.nombre_usuario} ({self.nombre}) - Email: {self.email} - Rol: {self.rol}"

    def to_dict(self):
        return to_dict(self)


class ProgramacionDia(EmbeddedDocument):
    dia = StringField(required=True)
    hora_inicio = StringField(required=True)
    duracion_minutos = IntField(required=True)
    humedad_objetivo = FloatField(required=True)
    ph_minimo = FloatField(required=True)
    ph_maximo = FloatField(required=True)
    temperatura_maxima = FloatField(required=True)

    def __str__(self):
        return (f"ProgramacionDia: {self.dia} {self.hora_inicio} duracion {self.duracion_minutos} min "
                f"Humedad {self.humedad_objetivo} pH [{self.ph_minimo}-{self.ph_maximo}] Temp max {self.temperatura_maxima}")

    def to_dict(self):
        # EmbeddedDocument no tiene .to_mongo, convertimos manualmente
        return {
            'dia': self.dia,
            'hora_inicio': self.hora_inicio,
            'duracion_minutos': self.duracion_minutos,
            'humedad_objetivo': self.humedad_objetivo,
            'ph_minimo': self.ph_minimo,
            'ph_maximo': self.ph_maximo,
            'temperatura_maxima': self.temperatura_maxima,
        }


class ZonaRiego(Document):
    usuario = ReferenceField(Usuario, required=False)
    nombre = StringField(required=True)
    ubicacion = StringField()
    fecha_creacion = DateTimeField(default=lambda: datetime.datetime.now(datetime.timezone.utc))

    # meta = {
    #     'collection': 'setup'
    # }

    def __str__(self):
        return f"ZonaRiego: {self.nombre} (Usuario: {self.usuario.nombre_usuario if self.usuario else 'N/A'})"

    def to_dict(self):
        d = to_dict(self)
        # Agregar usuario como dict o solo su id
        if self.usuario:
            d['usuario'] = str(self.usuario.id)
        return d


class Nodo(Document):
    zona = ReferenceField(ZonaRiego, required=True)
    nombre = StringField(required=True)
    descripcion = StringField()
    coordenadas = PointField(required=True)

    # meta = {
    #     'collection': 'setup'
    # }

    def __str__(self):
        return f"Nodo: {self.nombre} (Zona: {self.zona.nombre})"

    def to_dict(self):
        d = to_dict(self)
        d['zona'] = str(self.zona.id)
        return d


class Sensor(Document):
    nodo = ReferenceField(Nodo, required=True)
    tipo = StringField(required=True)
    modelo = StringField(required=True)
    descripcion = StringField()

    # meta = {
    #     'collection': 'setup'
    # }

    def __str__(self):
        return f"Sensor: {self.tipo} modelo {self.modelo} (Nodo: {self.nodo.nombre})"

    def to_dict(self):
        d = to_dict(self)
        d['nodo'] = str(self.nodo.id)
        return d


class Regador(Document):
    nodo = ReferenceField(Nodo, required=True)
    modelo = StringField(required=True)
    descripcion = StringField()

    # meta = {
    #     'collection': 'setup'
    # }

    def __str__(self):
        return f"Regador: modelo {self.modelo} (Nodo: {self.nodo.nombre})"

    def to_dict(self):
        d = to_dict(self)
        d['nodo'] = str(self.nodo.id)
        return d


class ConfiguracionRiego(Document):
    zona = ReferenceField(ZonaRiego, required=True)
    programacion = EmbeddedDocumentField(ProgramacionDia)

    # meta = {
    #     'collection': 'setup'
    # }

    def __str__(self):
        return f"ConfiguracionRiego para Zona: {self.zona.nombre} - {str(self.programacion)}"

    def to_dict(self):
        d = to_dict(self)
        d['zona'] = str(self.zona.id)
        d['programacion'] = self.programacion.to_dict() if self.programacion else None
        return d


class Sugerencia(Document):
    IMPACTO_CHOICES = ('bajo', 'medio', 'alto')
    zona = ReferenceField(ZonaRiego, required=True)
    fecha = DateTimeField(default=lambda: datetime.datetime.now(datetime.timezone.utc))
    mensaje = StringField(required=True)
    impacto = StringField(choices=IMPACTO_CHOICES)

    # meta = {
    #     'collection': 'setup'
    # }

    def __str__(self):
        return f"Sugerencia ({self.impacto}) en zona {self.zona.nombre}: {self.mensaje}"

    def to_dict(self):
        d = to_dict(self)
        d['zona'] = str(self.zona.id)
        return d


class LecturaSensor(Document):
    sensor = ReferenceField(Sensor, required=True)
    nodo = ReferenceField(Nodo, required=True)
    zona = ReferenceField(ZonaRiego, required=True)
    tipo = StringField(required=True)
    valor = FloatField(required=True)
    unidad = StringField(required=True)
    fecha_hora = DateTimeField(default=lambda: datetime.datetime.now(datetime.timezone.utc))

    meta = {
        'collection': 'history'
    }

    def __str__(self):
        return (f"LecturaSensor: {self.tipo} valor {self.valor}{self.unidad} "
                f"(Sensor: {self.sensor.tipo} Nodo: {self.nodo.nombre} Zona: {self.zona.nombre}) "
                f"Fecha: {self.fecha_hora.isoformat()}")

    def to_dict(self):
        d = to_dict(self)
        d['sensor'] = str(self.sensor.id)
        d['nodo'] = str(self.nodo.id)
        d['zona'] = str(self.zona.id)
        return d


class RegistroRiego(Document):
    regador = ReferenceField(Regador, required=True)
    nodo = ReferenceField(Nodo, required=True)
    zona = ReferenceField(ZonaRiego, required=True)
    cantidad_agua_litros = FloatField(required=True)
    energia_consumida_kwh = FloatField(required=True)
    duracion_segundos = IntField(required=True)
    fecha_hora_inicio = DateTimeField(required=True)
    fecha_hora_fin = DateTimeField(required=True)

    meta = {
        'collection': 'history'
    }

    def __str__(self):
        return (f"RegistroRiego: {self.cantidad_agua_litros} litros (Regador: {self.regador.modelo}) "
                f"Nodo: {self.nodo.nombre} Zona: {self.zona.nombre} "
                f"Inicio: {self.fecha_hora_inicio.isoformat()} Fin: {self.fecha_hora_fin.isoformat()}")

    def to_dict(self):
        d = to_dict(self)
        d['regador'] = str(self.regador.id)
        d['nodo'] = str(self.nodo.id)
        d['zona'] = str(self.zona.id)
        return d
