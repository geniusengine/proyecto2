import mysql.connector
from mysql.connector import Error

host = 'causas.mysql.database.azure.com'
usuario = 'admin_carlos'
contraseña = 'F14tomcat'
base_de_datos = 'matias1'

def crear_tabla_historial():
    """Función para crear la tabla Historial en la base de datos MySQL en Azure"""
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
            
            # Comprobar si la tabla ya existe
            cursor.execute("SHOW TABLES LIKE 'Historial'")
            result = cursor.fetchone()
            
            if result:
                print("La tabla 'Historial' ya existe.")
            else:
                # Crear la tabla Historial
                crear_tabla_query = """
                CREATE TABLE Historial (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    usuario_id INT NOT NULL,
                    accion VARCHAR(255) NOT NULL,
                    fecha_hora DATETIME DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (usuario_id) REFERENCES auth_user(id) ON DELETE CASCADE
                );
                """
                cursor.execute(crear_tabla_query)
                print("Tabla 'Historial' creada exitosamente.")
                
            # Cerrar el cursor
            cursor.close()

    except Error as e:
        print(f"Error al intentar conectar o crear la tabla: {e}")
    finally:
        if conexion.is_connected():
            conexion.close()
            print("La conexión ha sido cerrada")

# Ejecutar la función
crear_tabla_historial()
