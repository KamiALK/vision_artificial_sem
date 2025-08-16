# aqui tenemos como es la creacion de base de datos
#
#
# https://github.com/KamiALK/spartanv2/blob/gregory/fastapi/db/conection.py
#
# por favor observa como re sealiza la conexion
# requiere un archivo .env
# reemplazar el valor de .env.example y quitar el.example
#
#
# en claso de que elijas la instalcion de mongo dejo la documentacion
# https://www.mongodb.com/docs/mongodb-shell/install/
#
#
# documentarion for connection with mongo
# https://www.mongodb.com/docs/drivers/motor/
#


#!----------------------------------
from sqlalchemy import create_engine

from sqlalchemy.orm import sessionmaker, Session
from dotenv import load_dotenv
import os

load_dotenv()
DB_NAME = os.getenv("DB_NAME")
DB_HOST = os.getenv("DB_HOST")
DB_DIALECT = os.getenv("DB_DIALECT")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_USER = os.getenv("DB_USER")
DB_PORT = os.getenv("DB_PORT")


# todo lo referente a la conexion
URL_CONECTION = f"{DB_DIALECT}://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
engine = create_engine(
    URL_CONECTION,
)
Session = sessionmaker(autoflush=False, autocommit=False, bind=engine)


# comentado porque esta pendiente de implementeAR
# Base.metadata.create_all(bind=engine)
# Session.close_all()
