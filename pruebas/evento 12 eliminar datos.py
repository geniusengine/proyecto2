import mysql.connector
from mysql.connector import Error

# Datos de conexión
host = 'causas.mysql.database.azure.com'
usuario = 'admin_carlos'
contraseña = 'F14tomcat'
base_de_datos = 'matias1'

# Código del evento
evento_sql = """
CREATE EVENT IF NOT EXISTS EliminarNotificaciones
ON SCHEDULE EVERY 12 MINUTE
DO
    DELETE FROM notificacion
    WHERE estadoNoti = 1 AND UltimaActualizacionEstadoNoti < (NOW() - INTERVAL 12 MINUTE);
"""

def crear_evento():
    try:
        # Conectar a la base de datos
        conexion = mysql.connector.connect(
            host=host,
            user=usuario,
            password=contraseña,
            database=base_de_datos
        )

        if conexion.is_connected():
            cursor = conexion.cursor()
            # Ejecutar el código para crear el evento
            cursor.execute(evento_sql)
            print("Evento 'EliminarNotificaciones' creado exitosamente.")
            cursor.close()
        else:
            print("No se pudo conectar a la base de datos.")

    except Error as e:
        print(f"Error al crear el evento: {e}")

    finally:
        if conexion.is_connected():
            conexion.close()
            print("Conexión cerrada.")

# Ejecutar la función para crear el evento
crear_evento()
