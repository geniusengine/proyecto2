import mysql.connector
from mysql.connector import Error

host = 'causas.mysql.database.azure.com'  # Cambia esto por tu host de Azure
usuario = 'admin_carlos'     # Cambia esto por tu usuario
contraseña = 'F14tomcat'  # Cambia esto por tu contraseña
base_de_datos = 'matias1'  # Cambia esto por tu base de datos

def conectar_y_listar_tablas():
    """Función para conectarse a la base de datos MySQL en Azure y listar las tablas"""
    try:
        conexion = mysql.connector.connect(
            host=host, 
            user=usuario,
            password=contraseña,
            database=base_de_datos
        )
        if conexion.is_connected():
            print("Conexión exitosa a la base de datos")
            
            # Crear un cursor para ejecutar consultas
            cursor = conexion.cursor()
            cursor.execute("SHOW TABLES")
            
            # Obtener y mostrar todas las tablas
            tablas = cursor.fetchall()
            if tablas:
                print("Tablas en la base de datos:")
                for tabla in tablas:
                    print(tabla[0])  # Mostrar el nombre de cada tabla
            else:
                print("No hay tablas en la base de datos.")
            
            # Cerrar el cursor
            cursor.close()
        else:
            print("No se pudo conectar a la base de datos")

    except Error as e:
        print(f"Error al intentar conectar: {e}")
    finally:
        if conexion.is_connected():
            conexion.close()
            print("La conexión ha sido cerrada")

# Ejecutar la función
conectar_y_listar_tablas()

