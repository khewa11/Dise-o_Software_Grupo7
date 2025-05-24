import os
from dotenv import load_dotenv
import psycopg2
from datetime import datetime

# Cargar variables de entorno desde el archivo .env
load_dotenv()

####################################################
db_host = os.getenv('DB_HOST')
db_port = os.getenv('DB_PORT')
db_name = os.getenv('DB_NAME')
db_user = os.getenv('DB_USER')
db_pass = os.getenv('DB_PASS')

####################################################
connection = psycopg2.connect(
    host=db_host,
    port=db_port,
    database=db_name,
    user=db_user,
    password=db_pass
)

def ver_tablas():
    with connection.cursor() as cursor:
        cursor.execute(
            """
            SELECT table_name
              FROM information_schema.tables
             WHERE table_schema = 'public';
            """
        )
        tablas = cursor.fetchall()
        for tabla in tablas:
            nombre_tabla = tabla[0]
            print(f"\nTabla: {nombre_tabla}")

            try:
                cursor.execute(
                    f"SELECT * FROM {nombre_tabla};"
                )
                filas = cursor.fetchall()
                columnas = [desc[0] for desc in cursor.description]
                print("Columnas:", columnas)

                for fila in filas:
                    print(fila)

            except Exception as e:
                print(f"No se pudo consultar la tabla {nombre_tabla}:", e)


def incluir_usuario(id, nombre, correo, tipo_usuario):
    fecha_registro = datetime.now()
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO usuario (id, nombre, correo, tipo_usuario, fecha_registro)
                VALUES (%s, %s, %s, %s, %s);
                """,
                (id, nombre, correo, tipo_usuario, fecha_registro)
            )


def incluir_paquete(id, peso, dimensiones, fecha_envio, usuario_id, estado_entrega_id, ruta_id):
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO paquete (id, peso, dimensiones, fecha_envio, usuario_id, estado_entrega_id, ruta_id)
                VALUES (%s, %s, %s, %s, %s, %s, %s);
                """,
                (id, peso, dimensiones, fecha_envio, usuario_id, estado_entrega_id, ruta_id)
            )


def incluir_ruta(id, origen, destino, distancia_km, duracion_estimada_min):
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO ruta (id, origen, destino, distancia_km, duracion_estimada_min)
                VALUES (%s, %s, %s, %s, %s);
                """,
                (id, origen, destino, distancia_km, duracion_estimada_min)
            )


if __name__ == '__main__':
    # Ejemplo de uso
    ver_tablas()
    connection.close()

    connection.close()
