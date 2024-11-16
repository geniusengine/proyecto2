import mysql.connector
from mysql.connector import Error

host = 'causas.mysql.database.azure.com'
usuario = 'admin_carlos'
contraseña = 'F14tomcat'
base_de_datos = 'matias1'

def insertar_usuario():
    """Función para insertar un usuario en la tabla 'usuarios'"""
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
            
            # Insertar usuario con el nombre "Randy"
            query = """
            INSERT INTO usuarios (username, nombreusuario, apellidousuario, password)
            VALUES (%s, %s, %s, %s)
            """
            valores = ('Randy', 'Randy', 'Randy', 'Randy')
            
            cursor.execute(query, valores)
            conexion.commit()
            
            print("Usuario 'Randy' insertado correctamente.")
            
            # Cerrar cursor
            cursor.close()
        else:
            print("No se pudo conectar a la base de datos.")

    except Error as e:
        print(f"Error al intentar insertar el usuario: {e}")
    
    finally:
        if conexion.is_connected():
            conexion.close()
            print("Conexión cerrada.")

# Ejecutar la función para insertar el usuario
insertar_usuario()
