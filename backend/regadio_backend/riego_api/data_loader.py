# riego_api/data_loader.py
import json
from pathlib import Path
from .models import (
    Usuario, ZonaRiego, Nodo, Sensor, LecturaSensor,
    Sugerencia, ConfiguracionRiego, Regador, RegistroRiego,
    ProgramacionDia
)

FAKE_DATA_PATH = Path(__file__).resolve().parent.parent / "fakedata.json"

def cargar_datos_fake():
    with open(FAKE_DATA_PATH, encoding="utf-8") as f:
        raw = json.load(f)

    objetos = {}

    # Usuarios
    objetos["usuarios"] = [Usuario(**u) for u in raw.get("usuarios", [])]

    # Zonas de riego (conectadas a usuarios)
    user_map = {u.nombre_usuario: u for u in objetos["usuarios"]}
    objetos["zonas_riego"] = [
        ZonaRiego(**{**z, "usuario": user_map[z["usuario"]]})
        for z in raw.get("zonas_riego", [])
    ]

    zona_map = {z.nombre: z for z in objetos["zonas_riego"]}

    # Nodos
    objetos["nodos"] = [
        Nodo(**{**n, "zona_id": zona_map[n["zona_id"]]})
        for n in raw.get("nodos", [])
    ]

    nodo_map = {n.nombre: n for n in objetos["nodos"]}

    # Sensores
    objetos["sensores"] = [
        Sensor(**{**s, "nodo_id": nodo_map[s["nodo_id"]]})
        for s in raw.get("sensores", [])
    ]

    sensor_map = {s.modelo: s for s in objetos["sensores"] if s.modelo}

    # Lecturas
    objetos["lecturas_sensor"] = [
        LecturaSensor(
            **{
                **l,
                "sensor_id": sensor_map[l["sensor_id"]],
                "nodo_id": nodo_map[l["nodo_id"]],
                "zona_id": zona_map[l["zona_id"]],
            }
        )
        for l in raw.get("lecturas_sensor", [])
    ]

    # Sugerencias
    objetos["sugerencias"] = [
        Sugerencia(**{**s, "zona_id": zona_map[s["zona_id"]]})
        for s in raw.get("sugerencias", [])
    ]

    # Configuraciones
    objetos["configuraciones_riego"] = []
    for c in raw.get("configuraciones_riego", []):
        prog = [ProgramacionDia(**d) for d in c.get("programacion", [])]
        config = ConfiguracionRiego(zona_id=zona_map[c["zona_id"]], programacion=prog)
        objetos["configuraciones_riego"].append(config)

    # Regadores
    objetos["regadores"] = [
        Regador(**{**r, "nodo_id": nodo_map[r["nodo_id"]]})
        for r in raw.get("regadores", [])
    ]
    regador_map = {r.modelo: r for r in objetos["regadores"] if r.modelo}

    # Registros de riego
    objetos["registros_riego"] = [
        RegistroRiego(
            **{
                **r,
                "regador_id": regador_map[r["regador_id"]],
                "nodo_id": nodo_map[r["nodo_id"]],
                "zona_id": zona_map[r["zona_id"]],
            }
        )
        for r in raw.get("registros_riego", [])
    ]

    return objetos
