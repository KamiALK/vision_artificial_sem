# from  sqlalchemy.orm import Session
# from conection import Session

from sqlalchemy import text
from connection import Session  # importa tu Session desde connection.py


def test_db():
    session = Session()  # abrir conexión
    try:
        # Consulta genérica que funciona en PostgreSQL, MySQL y la mayoría de motores
        result = session.execute(text("SELECT 1")).fetchone()
        print("✅ Conexión exitosa. Respuesta:", result[0])
    except Exception as e:
        print("❌ Error en la conexión:", e)
    finally:
        session.close()


if __name__ == "__main__":
    test_db()
# aqui la configuracion de la base de datos
# def get_db():
#     db = Session()
#     try:
#         yield db
#     finally:
#         db.close()
