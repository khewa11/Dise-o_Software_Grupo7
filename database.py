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
class Usuarios:
    def __init__(self, id, nombre, correo, tipo_usuario, fecha_registro):
        self.id = id
        self.nombre = nombre
        self.correo = correo
        self.tipo_usuario = tipo_usuario
        self.fecha_registro = fecha_registro

class Ruta:
    def __init__(self, id, origen, destino, distancia_km, duracion_estimada_min):
        self.id = id
        self.origen = origen
        self.destino = destino
        self.distancia_km = distancia_km
        self.duracion_estimada_min = duracion_estimada_min

class Paquete:
    def __init__(self, id, peso, dimensiones, fecha_envio, usuario_id, estado_entrega_id, ruta_id):
        self.id = id
        self.peso = peso
        self.dimensiones = dimensiones
        self.fecha_envio = fecha_envio
        self.usuario_id = usuario_id
        self.estado_entrega_id = estado_entrega_id
        self.ruta_id = ruta_id
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

def buscar_usuario(id):
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM usuario WHERE id = %s",(id,))
    rows = cursor.fetchall()
    if rows:
        usuario = Usuarios(rows[0][0], rows[0][1], rows[0][2], rows[0][3],rows[0][4])
        return usuario  
    else:
        print("usuario no encontrado.")
        return None

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
  
def buscar_paquete(id):
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM paquete WHERE id = %s", (id,))
    rows = cursor.fetchall()
    if rows:
        paquete = Paquete(rows[0][0],rows[0][1],rows[0][2],rows[0][3],rows[0][4],rows[0][5],rows[0][6])
        return paquete
    else:
        print("Paquete no encontrado.")
        return None

def cambiar_estado_paquete(paquete_id, nuevo_estado):
    if nuevo_estado not in (1, 2, 3):
        print("Estado no válido. Solo se permiten los valores 1, 2 o 3.")
        return

    cursor = connection.cursor()
    cursor.execute(
        "UPDATE paquete SET estado_entrega_id = %s WHERE id = %s",
        (nuevo_estado, paquete_id)
    )
    connection.commit()
    print(f"Estado del paquete {paquete_id} actualizado a {nuevo_estado}.")


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

def buscar_ruta(id):
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM ruta WHERE id = %s", (id,))
    rows = cursor.fetchall()
    if rows:
        ruta = Ruta(rows[0][0], rows[0][1], rows[0][2], rows[0][3], rows[0][4])
        return ruta
    else:
        print("Ruta no encontrada.")
        return None

if __name__ == '__main__':
    # Ejemplo de uso
    ver_tablas()
    connection.close()

    connection.close()
