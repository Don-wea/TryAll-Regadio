# mongoDB 


## Requirements

1. satisfacer los requerimientos previos, encontrados en el directorio  
   `Tryall-regadio/backend/README.md`

2. *mongoDB instalado ( Sólo en caso de no tener base de datos en la nube)  
Se utiliza la version 7.0.21, pero no deberian existir problemas de compatibilidad con versiones futuras.



## Funcionamiento

### --- Agregar datos 'dummy' a la base de datos ---

Ejecutar `agregar_datos_dummy.py` para la creacion de datos dummy en tu base de datos local *(en caso de que no hayan datos y se este trabajando con una base de datos local)*

### --- Conectar a una base de datos diferente ---

En el archivo `TryAll-Regadio/backend/regadio_backend/regadio_backend/settings.py`, dirigirse a la seccion de database, y encontraras lo siguiente:

```bash
# ----- Database -----

# Conexión a MongoDB
MONGODB_HOST = 'localhost'
MONGODB_PORT = 27017
MONGODB_NAME = 'regadio_db'

```
Aqui sustituir los puertos, el host y el nombre de la base de datos por los que se deseen utilizar.

- **Lista de bases de datos:**  

  - local  

    - MONGODB_HOST = 'localhost'  
    - MONGODB_PORT = 27017  (puerto por defecto pero puede variar)  
    - MONGODB_NAME = 'regadio_db'  
    
  - https://mongo.podlech.dev/  

    - username: admin  
    - password: ADMIN  



## Comandos

| Acción  | Linux              | Windows               |
|:-----------|:---------------------|:----------------------------|
|Ver estado de MongoDB|`sudo systemctl status mongod`|`sc query MongoDB`|
|Iniciar servicio| `sudo systemctl start mongod`| `net start MongoDB`|
|Iniciar manual desde binario| `mongod` (según ruta de instalación)|`"C:\Program Files\MongoDB\Server\7.0\bin\mongod.exe"`|
|Abrir shell de MongoDB| `mongosh`| `mongosh`|
|Poblar base con datos dummy| `python scripts/seed_db.py`| `python scripts/seed_db.py`|