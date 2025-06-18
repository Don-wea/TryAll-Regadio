# ❖ ❖ ❖ ❖ ❖ IMPORTS ❖ ❖ ❖ ❖ ❖
from mongoengine import connect

# importar datos dummy
from datos_dummy import martitax 



# ❖ ❖ ❖ ❖ ❖ Informacion de las bases de datos ❖ ❖ ❖ ❖ ❖

# BASE DE DATOS: regadio_db local
DATABASE_NAME = "regadio_db"  # Cambia por el nombre de tu base si quieres
DATABASE_HOST = "localhost"
DATABASE_PORT = 27017

#BASE DE DATOS: regadio_db en MongoDB Atlas
# DATABASE_NAME = "regadio_db"
# DATABASE_HOST = "cluster0.mongodb.net"  # Cambia por tu host de Atlas
# DATABASE_PORT = 27017  # MongoDB Atlas usa el puerto 27017 por

#BASE DE DATOS: mongo.podlech.dev
# los datos de la base de datos del podlech (parece estar desconectada)



# ❖ ❖ ❖ ❖ ❖ Conexión a la base de datos ❖ ❖ ❖ ❖ ❖
connect(
    db=DATABASE_NAME,          
    host=DATABASE_HOST,
    port=DATABASE_PORT
)



# ❖ ❖ ❖ ❖ ❖ Datos Dummy para poblar la base de datos ❖ ❖ ❖ ❖ ❖

martitax.poblar()
'''  cuenta con
1 usuario,
1 zona de riego,
1 nodo,
1 sensor,
1 regador,
1 configuracion de riego,
1 sugerencia,
10 registros de riego,
10 registros de sensor
'''