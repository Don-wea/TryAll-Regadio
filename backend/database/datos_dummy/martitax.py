import os
import sys
import bcrypt

def hash_password(password: str) -> str:
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')
def check_password(password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))


path_to_add = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../regadio_backend'))
print(f"Adding this path to sys.path: {path_to_add}")

sys.path.append(path_to_add)
import enum

from riego_api.models import (
    TipoSensor
)

from riego_api.models import (
    Usuario, ProgramacionDia, ZonaRiego, Nodo,
    Sensor, Regador, ConfiguracionRiego, Sugerencia,
    LecturaSensor, RegistroRiego
)

import datetime
import random


def ZonaCentral(usuario1):
    # --- Zonas ---
    zona1 = ZonaRiego(
        usuario_id=usuario1,
        nombre="Zona Central",
        ubicacion="Sector A"
    )
    zona1.save()
    print(f"Zona de Riego creada: {zona1}")


    # --- Nodos ---
    nodo1 = Nodo(
        zona_id=zona1,
        nombre="Nodo Principal",
        descripcion="Nodo de control central",
        coordenadas={"type": "Point", "coordinates": [68.6483, 67.4569]}
    )
    nodo1.save()
    print(f"Nodo creado: {nodo1}")


    # --- Sensores ---
    sensor1 = Sensor(
        nodo_id=nodo1,
        tipo='humedad_suelo',
        modelo="HMD-100",
        descripcion="Sensor de humedad del suelo"
    )
    sensor1.save()
    print(f"Sensor creado: {sensor1}")


    # --- Regadores ---
    regador1 = Regador(
        nodo_id=nodo1,
        modelo="RGD-200",
        descripcion="Regador automático por aspersión"
    )
    regador1.save()
    print(f"Regador creado: {regador1}")


    # --- Programación y Configuración de Riego ---
    programacion1 = ProgramacionDia(
        dia="Lunes",
        hora_inicio="06:00",
        duracion_minutos=30,
        humedad_objetivo=70.0,
        ph_minimo=6.0,
        ph_maximo=7.0,
        temperatura_maxima=30.0
    )

    configuracion1 = ConfiguracionRiego(
        zona_id=zona1,
        programacion=programacion1
    )
    configuracion1.save()
    print(f"Configuración de Riego creada: {configuracion1}")


    # --- Sugerencias ---
    sugerencia1 = Sugerencia(
        zona_id=zona1,
        mensaje="Se recomienda disminuir agua en días lluviosos",
        impacto="bajo"
    )
    sugerencia1.save()
    print(f"Sugerencia creada: {sugerencia1}")



    # --- 10 Lecturas de Sensor y 10 Registros de Riego ---
    for i in range(10):
        fecha_base = datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(days=i)


        # Lectura Sensor
        lectura = LecturaSensor(
            sensor_id=sensor1,
            nodo_id=nodo1,
            zona_id=zona1,
            tipo="humedad_suelo",
            valor=round(random.uniform(60.0, 80.0), 2),
            unidad="%",
            fecha_hora=fecha_base
        )
        lectura.save()
        print(f"Lectura Sensor {i+1} creada: {lectura.valor}% en {fecha_base.date()}")


        # Registro de Riego
        inicio_riego = fecha_base.replace(hour=6, minute=0)
        fin_riego = inicio_riego + datetime.timedelta(minutes=30)
        registro_riego = RegistroRiego(
            regador_id=regador1,
            nodo_id=nodo1,
            zona_id=zona1,
            cantidad_agua_litros=round(random.uniform(45.0, 55.0), 2),
            energia_consumida_kwh=round(random.uniform(0.4, 0.6), 2),
            duracion_segundos=1800,
            fecha_hora_inicio=inicio_riego,
            fecha_hora_fin=fin_riego
        )
        registro_riego.save()
        print(f"Registro de Riego {i+1} creado: {registro_riego.cantidad_agua_litros}L el {inicio_riego.date()}")

def ZonaSur(usuario1):
    # --- Zonas ---
    zona1 = ZonaRiego(
        usuario_id=usuario1,
        nombre="Chillan",
        ubicacion="Sector D"
    )
    zona1.save()
    print(f"Zona de Riego creada: {zona1}")


    # --- Nodos ---
    nodo1 = Nodo(
        zona_id=zona1,
        nombre="Nodo Principal",
        descripcion="Nodo de control periferico",
        coordenadas={"type": "Point", "coordinates": [70.6483, -43.4569]}
    )
    nodo1.save()
    print(f"Nodo creado: {nodo1}")


    # --- Sensores ---
    sensor1 = Sensor(
        nodo_id=nodo1,
        tipo="Humedad",
        modelo="HMD-100",
        descripcion="Sensor de humedad del suelo"
    )
    sensor1.save()
    print(f"Sensor creado: {sensor1}")


    # --- Regadores ---
    regador1 = Regador(
        nodo_id=nodo1,
        modelo="RGD-200",
        descripcion="Regador automático por aspersión"
    )
    regador1.save()
    print(f"Regador creado: {regador1}")


    # --- Programación y Configuración de Riego ---
    programacion1 = ProgramacionDia(
        dia="Lunes",
        hora_inicio="06:00",
        duracion_minutos=30,
        humedad_objetivo=70.0,
        ph_minimo=6.0,
        ph_maximo=7.0,
        temperatura_maxima=30.0
    )

    configuracion1 = ConfiguracionRiego(
        zona_id=zona1,
        programacion=programacion1
    )
    configuracion1.save()
    print(f"Configuración de Riego creada: {configuracion1}")


    # --- Sugerencias ---
    sugerencia1 = Sugerencia(
        zona_id=zona1,
        mensaje="Se recomienda ajustar el riego en días calurosos",
        impacto="medio"
    )
    sugerencia1.save()
    print(f"Sugerencia creada: {sugerencia1}")



    # --- 10 Lecturas de Sensor y 10 Registros de Riego ---
    for i in range(10):
        fecha_base = datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(days=i)


        # Lectura Sensor
        lectura = LecturaSensor(
            sensor_id=sensor1,
            nodo_id=nodo1,
            zona_id=zona1,
            tipo="humedad_suelo",
            valor=round(random.uniform(60.0, 80.0), 2),
            unidad="%",
            fecha_hora=fecha_base
        )
        lectura.save()
        print(f"Lectura Sensor {i+1} creada: {lectura.valor}% en {fecha_base.date()}")


        # Registro de Riego
        inicio_riego = fecha_base.replace(hour=6, minute=0)
        fin_riego = inicio_riego + datetime.timedelta(minutes=30)
        registro_riego = RegistroRiego(
            regador_id=regador1,
            nodo_id=nodo1,
            zona_id=zona1,
            cantidad_agua_litros=round(random.uniform(45.0, 55.0), 2),
            energia_consumida_kwh=round(random.uniform(0.4, 0.6), 2),
            duracion_segundos=1800,
            fecha_hora_inicio=inicio_riego,
            fecha_hora_fin=fin_riego
        )
        registro_riego.save()
        print(f"Registro de Riego {i+1} creado: {registro_riego.cantidad_agua_litros}L el {inicio_riego.date()}")



    # ----- Nodo 2 -----
    nodo2 = Nodo(
        zona_id=zona1,
        nombre="Nodo Principal",
        descripcion="Nodo de control central",
        coordenadas={"type": "Point", "coordinates": [70.6483, -43.4569]}
    )
    nodo2.save()
    print(f"Nodo creado: {nodo2}")

    # --- Sensores ---
    sensor2_1 = Sensor(
        nodo_id=nodo2,
        tipo="humedad_suelo",
        modelo="HMD-100",
        descripcion="Sensor de humedad del suelo"
    )
    sensor2_1.save()
    print(f"Sensor creado: {sensor2_1}")


    # --- Regadores ---
    regador2_1 = Regador(
        nodo_id=nodo2,
        modelo="RGD-200",
        descripcion="Regador automático por aspersión"
    )
    regador2_1.save()
    print(f"Regador creado: {regador2_1}")


    # --- Programación y Configuración de Riego ---
    programacion1 = ProgramacionDia(
        dia="Lunes",
        hora_inicio="06:00",
        duracion_minutos=30,
        humedad_objetivo=70.0,
        ph_minimo=6.0,
        ph_maximo=7.0,
        temperatura_maxima=30.0
    )

    configuracion1 = ConfiguracionRiego(
        zona_id=zona1,
        programacion=programacion1
    )
    configuracion1.save()
    print(f"Configuración de Riego creada: {configuracion1}")


    # --- Sugerencias ---
    sugerencia1 = Sugerencia(
        zona_id=zona1,
        mensaje="Se recomienda ajustar el riego en días calurosos",
        impacto="medio"
    )
    sugerencia1.save()
    print(f"Sugerencia creada: {sugerencia1}")



    # --- 10 Lecturas de Sensor y 10 Registros de Riego ---
    for i in range(10):
        fecha_base = datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(days=i)


        # Lectura Sensor
        lectura = LecturaSensor(
            sensor_id=sensor2_1,
            nodo_id=nodo2,
            zona_id=zona1,
            tipo="humedad_suelo",
            valor=round(random.uniform(60.0, 80.0), 2),
            unidad="%",
            fecha_hora=fecha_base
        )
        lectura.save()
        print(f"Lectura Sensor {i+1} creada: {lectura.valor}% en {fecha_base.date()}")


        # Registro de Riego
        inicio_riego = fecha_base.replace(hour=6, minute=0)
        fin_riego = inicio_riego + datetime.timedelta(minutes=30)
        registro_riego = RegistroRiego(
            regador_id=regador2_1,
            nodo_id=nodo2,
            zona_id=zona1,
            cantidad_agua_litros=round(random.uniform(45.0, 55.0), 2),
            energia_consumida_kwh=round(random.uniform(0.4, 0.6), 2),
            duracion_segundos=1800,
            fecha_hora_inicio=inicio_riego,
            fecha_hora_fin=fin_riego
        )
        registro_riego.save()
        print(f"Registro de Riego {i+1} creado: {registro_riego.cantidad_agua_litros}L el {inicio_riego.date()}")


def poblar():
    # --- Usuario ---
    usuario1 = Usuario(
        nombre_usuario="martitax",
        nombre="Marta G",
        email="marta@example.com",
        password_hash=hash_password("marta123"),
    )
    usuario1.save()
    print(f"Usuario creado: {usuario1}")

    ZonaCentral(usuario1)
    ZonaSur(usuario1)
    
if __name__ == "__main__":
    poblar()
