# riego_api/data_loader.py
import json
from pathlib import Path
from bson import ObjectId
from .models import (
    Usuario, ZonaRiego, Nodo, Sensor, LecturaSensor,
    Sugerencia, ConfiguracionRiego, Regador, RegistroRiego,
    ProgramacionDia
)

FAKE_DATA_PATH = Path(__file__).resolve().parent.parent / "fakedata.json"

class FakeDataContainer:
    """
    Contenedor para los datos fake que simula las colecciones de MongoDB
    """
    def __init__(self):
        self.usuarios = []
        self.zonas_riego = []
        self.nodos = []
        self.sensores = []
        self.lecturas_sensor = []
        self.sugerencias = []
        self.configuraciones_riego = []
        self.regadores = []
        self.registros_riego = []

def cargar_datos_fake():
    with open(FAKE_DATA_PATH, encoding="utf-8") as f:
        raw = json.load(f)

    container = FakeDataContainer()

    # Usuarios
    for u in raw.get("usuarios", []):
        usuario = Usuario(**u)
        usuario._id = ObjectId()  # Asignar un ID único
        container.usuarios.append(usuario)

    # Zonas de riego (conectadas a usuarios)
    user_map = {u.nombre_usuario: u for u in container.usuarios}
    for z in raw.get("zonas_riego", []):
        zona = ZonaRiego(**{**z, "usuario": user_map[z["usuario"]]})
        zona._id = ObjectId()  # Asignar un ID único
        container.zonas_riego.append(zona)

    zona_map = {z.nombre: z for z in container.zonas_riego}

    # Nodos
    for n in raw.get("nodos", []):
        nodo = Nodo(**{**n, "zona_id": zona_map[n["zona_id"]]})
        nodo._id = ObjectId()  # Asignar un ID único
        container.nodos.append(nodo)

    nodo_map = {n.nombre: n for n in container.nodos}

    # Sensores
    for s in raw.get("sensores", []):
        sensor = Sensor(**{**s, "nodo_id": nodo_map[s["nodo_id"]]})
        sensor._id = ObjectId()  # Asignar un ID único
        container.sensores.append(sensor)

    sensor_map = {s.modelo: s for s in container.sensores if s.modelo}

    # Lecturas
    for l in raw.get("lecturas_sensor", []):
        lectura = LecturaSensor(
            **{
                **l,
                "sensor_id": sensor_map[l["sensor_id"]],
                "nodo_id": nodo_map[l["nodo_id"]],
                "zona_id": zona_map[l["zona_id"]],
            }
        )
        lectura._id = ObjectId()  # Asignar un ID único
        container.lecturas_sensor.append(lectura)

    # Sugerencias
    for s in raw.get("sugerencias", []):
        sugerencia = Sugerencia(**{**s, "zona_id": zona_map[s["zona_id"]]})
        sugerencia._id = ObjectId()  # Asignar un ID único
        container.sugerencias.append(sugerencia)

    # Configuraciones
    for c in raw.get("configuraciones_riego", []):
        prog = [ProgramacionDia(**d) for d in c.get("programacion", [])]
        config = ConfiguracionRiego(zona_id=zona_map[c["zona_id"]], programacion=prog)
        config._id = ObjectId()  # Asignar un ID único
        container.configuraciones_riego.append(config)

    # Regadores
    for r in raw.get("regadores", []):
        regador = Regador(**{**r, "nodo_id": nodo_map[r["nodo_id"]]})
        regador._id = ObjectId()  # Asignar un ID único
        container.regadores.append(regador)

    regador_map = {r.modelo: r for r in container.regadores if r.modelo}

    # Registros de riego
    for r in raw.get("registros_riego", []):
        registro = RegistroRiego(
            **{
                **r,
                "regador_id": regador_map[r["regador_id"]],
                "nodo_id": nodo_map[r["nodo_id"]],
                "zona_id": zona_map[r["zona_id"]],
            }
        )
        registro._id = ObjectId()  # Asignar un ID único
        container.registros_riego.append(registro)

    return container