import mysql.connector
from mysql.connector import Error

def conectar_y_obtener_usuarios():
    """Función para conectarse a la base de datos MySQL en Azure y obtener los datos de la tabla usuarios"""
    conexion = None  # Definir 'conexion' como None
    try:
        conexion = mysql.connector.connect(
            host='causas.mysql.database.azure.com', 
            user='admin_carlos',
            password='F14tomcat',
            database='matias1'
        )
        if conexion.is_connected():
            print("Conexión exitosa a la base de datos")
            
            # Crear un cursor para ejecutar consultas
            cursor = conexion.cursor()
            
            # Ejecutar consulta para obtener datos de la tabla 'usuarios'
            cursor.execute("SELECT * FROM usuarios")
            
            # Obtener y mostrar todos los registros de la tabla 'usuarios'
            usuarios = cursor.fetchall()
            if usuarios:
                print("Contenido de la tabla 'usuarios':")
                for usuario in usuarios:
                    print(usuario)  # Mostrar cada registro
            else:
                print("La tabla 'usuarios' está vacía.")
            
            # Cerrar el cursor
            cursor.close()
        else:
            print("No se pudo conectar a la base de datos")

    except Error as e:
        print(f"Error al intentar conectar: {e}")
    finally:
        # Verificar que la conexión esté establecida antes de intentar cerrarla
        if conexion is not None and conexion.is_connected():
            conexion.close()
            print("La conexión ha sido cerrada")

# Ejecutar la función
conectar_y_obtener_usuarios()
