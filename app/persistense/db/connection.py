# aqui tenemos como es la creacion de base de datos
#
#
# https://github.com/KamiALK/spartanv2/blob/gregory/fastapi/db/conection.py
#
# por favor observa como re sealiza la conexion
# requiere un archivo .env
# reemplazar el valor de .env.example y quitar el.example
#
# ######################## joel avances  #######################33
#
#
#
# reunion de avances persistencia
# https://hub.docker.com/_/mongo
#
# https://www.mongodb.com/docs/languages/python/pymongo-driver/current/connect/#std-label-pymongo-connect
#
# en caso de conectar a una base de datos de mongo attlas usar el siguinete enlac e
#
# https://www.mongodb.com/docs/languages/python/pymongo-driver/current/get-started/#std-label-pymongo-get-started
from pymongo import MongoClient

# "mongodb://<db_username>:<db_password>@<hostname>:<port>"
try:
    db = "ip_contenedor de base de datos"
    client = MongoClient(
        "mongodb://root:example@192.168.144.3:27017/",
    )

    client.admin.command("ping")

    print("Connected successfully")

    client.close()
except Exception as e:
    # logica para errores del programa
    print(e)
