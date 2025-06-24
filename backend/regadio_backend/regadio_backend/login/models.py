from mongoengine import Document, StringField, EmailField, DateTimeField
from datetime import datetime, timezone

# class Usuario(Document):
#     nombre_usuario = StringField(required=True, unique=True)
#     nombre = StringField(required=True)
#     email = EmailField(required=True, unique=True)
#     password_hash = StringField(required=True)
#     rol = StringField(required=True, choices=['admin', 'usuario'], default='usuario')
#     fecha_registro = DateTimeField(default=lambda: datetime.now(timezone.utc))

#     meta = {
#         'collection': 'usuarios'
#     }

#     def __str__(self):
#         return f"{self.nombre_usuario} ({self.nombre})"
