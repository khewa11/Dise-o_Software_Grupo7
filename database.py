import psycopg2
from datetime import datetime
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


connection = psycopg2.connect(
        host="shuttle.proxy.rlwy.net",  
        port=56202,                      
        database="railway",             
        user="postgres",   
        password="TmgcmXeCJiWEXnXGQbuvECJHnZXNdInt"
    )
def ver_tablas():
    cursor = connection.cursor()

    cursor.execute("""
        SELECT table_name
        FROM information_schema.tables
        WHERE table_schema = 'public';
    """)
    tablas = cursor.fetchall()  
    for tabla in tablas:
        nombre_tabla = tabla[0]
        print(f"\nTabla: {nombre_tabla}")

        try:
            cursor.execute(f"SELECT * FROM {nombre_tabla};") 
            filas = cursor.fetchall()
            columnas = [desc[0] for desc in cursor.description]  
            print("Columnas:", columnas)

            for fila in filas:
                print(fila)

        except Exception as e:
            print(f"No se pudo consultar la tabla {nombre_tabla}:", e)

    cursor.close()  

def incluir_usuario(id, nombre, correo, tipo_usuario):
    cursor = connection.cursor()

    fecha_registro = datetime.now()

    cursor.execute("""
        INSERT INTO usuario (id, nombre, correo, tipo_usuario, fecha_registro)
        VALUES (%s, %s, %s, %s, %s);
    """, (id, nombre, correo, tipo_usuario, fecha_registro))
    connection.commit()
    cursor.close()

def incluir_paquete(id, peso, dimensiones, fecha_envio, usuario_id, estado_entrega_id, ruta_id):
    cursor = connection.cursor()
    cursor.execute("""
        INSERT INTO paquete (id, peso, dimensiones, fecha_envio, usuario_id, estado_entrega_id, ruta_id)
        VALUES (%s, %s, %s, %s, %s, %s, %s);
    """, (id, peso, dimensiones, fecha_envio, usuario_id, estado_entrega_id, ruta_id))

    connection.commit()
    cursor.close()
    
def incluir_ruta(id, origen, destino, distancia_km, duracion_estimada_min):

    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO ruta (id, origen, destino, distancia_km, duracion_estimada_min)
        VALUES (%s, %s, %s, %s, %s);
    """, (id, origen, destino, distancia_km, duracion_estimada_min))

    connection.commit()
    cursor.close()


if __name__ == '__main__':
    
  
  
    ver_tablas()
    connection.close()