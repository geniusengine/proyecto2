import mysql.connector
from mysql.connector import Error

host = 'causas.mysql.database.azure.com'
usuario = 'admin_carlos'
contraseña = 'F14tomcat'
base_de_datos = 'matias1'

def conectar_y_crear_tablas():
    """Función para conectarse a la base de datos 'matias1' y crear las tablas"""
    try:
        conexion = mysql.connector.connect(
            host=host,
            user=usuario,
            password=contraseña,
            database=base_de_datos
        )
        
        if conexion.is_connected():
            cursor = conexion.cursor()
            
            # Creación de las tablas
            tablas = {
                "actuaciones": """
                CREATE TABLE IF NOT EXISTS actuaciones (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    numjui VARCHAR(255),
                    nombTribunal VARCHAR(255),
                    tipojuicio VARCHAR(255),
                    actuacion VARCHAR(255),
                    fecha DATETIME,
                    UNIQUE (numjui, nombTribunal, tipojuicio, actuacion)
                );
                """,
                
                "AUD_notificacion": """
                CREATE TABLE IF NOT EXISTS AUD_notificacion (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    fechaNotificacion DATETIME,
                    numjui VARCHAR(255),
                    nombTribunal VARCHAR(255),
                    demandante VARCHAR(255),
                    demandado VARCHAR(255),
                    repre VARCHAR(255),
                    mandante VARCHAR(255),
                    domicilio VARCHAR(255),
                    comuna VARCHAR(255),
                    encargo VARCHAR(255),
                    soli VARCHAR(255),
                    arancel INT,
                    estadoNoti INT,
                    estadoCausa INT,
                    actu VARCHAR(255)
                );
                """,
                
                "buscar_historico": """
                CREATE TABLE IF NOT EXISTS buscar_historico (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    fechaNotificacion DATETIME,
                    numjui VARCHAR(255),
                    nombTribunal VARCHAR(255),
                    demandante VARCHAR(255),
                    demandado VARCHAR(255),
                    repre VARCHAR(255),
                    mandante VARCHAR(255),
                    domicilio VARCHAR(255),
                    comuna VARCHAR(255),
                    encargo VARCHAR(255),
                    soli VARCHAR(255),
                    arancel INT,
                    estadoNoti INT,
                    estadoCausa INT,
                    actu VARCHAR(255)
                );
                """,
                
                "demanda": """
                CREATE TABLE IF NOT EXISTS demanda (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    numjui VARCHAR(255),
                    nombTribunal VARCHAR(255),
                    demandante VARCHAR(255),
                    demandado VARCHAR(255),
                    repre VARCHAR(255),
                    mandante VARCHAR(255),
                    domicilio VARCHAR(255),
                    comuna VARCHAR(255),
                    encargo VARCHAR(255),
                    soli VARCHAR(255),
                    arancel INT,
                    actu VARCHAR(255),
                    UNIQUE (numjui, nombTribunal)
                );
                """,
                
                "historico": """
                CREATE TABLE IF NOT EXISTS historico (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    numJui VARCHAR(255),
                    tribunal VARCHAR(255),
                    tipoEstampado VARCHAR(255),
                    mandante VARCHAR(255),
                    arancel INT
                );
                """,
                
                "notificacion": """
                CREATE TABLE IF NOT EXISTS notificacion (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    fechaNotificacion DATETIME,
                    numjui VARCHAR(255),
                    nombTribunal VARCHAR(255),
                    demandante VARCHAR(255),
                    demandado VARCHAR(255),
                    repre VARCHAR(255),
                    mandante VARCHAR(255),
                    domicilio VARCHAR(255),
                    comuna VARCHAR(255),
                    encargo VARCHAR(255),
                    soli VARCHAR(255),
                    arancel INT,
                    estadoNoti INT,
                    estadoCausa INT,
                    actu VARCHAR(255)
                );
                """,
                
                "usuarios": """
                CREATE TABLE IF NOT EXISTS usuarios (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    username VARCHAR(225) NOT NULL,
                    nombreusuario VARCHAR(255) NOT NULL,
                    apellidousuario VARCHAR(255) NOT NULL,
                    password VARCHAR(255) NOT NULL
                );
                """
            }
            
            for nombre, query in tablas.items():
                cursor.execute(query)
                print(f"Tabla '{nombre}' creada o ya existe.")
            
            # Procedimiento almacenado
            cursor.execute("""
            CREATE PROCEDURE IF NOT EXISTS EliminarNotificaciones()
            BEGIN
                DELETE FROM notificacion
                WHERE estadoNoti = 1 AND UltimaActualizacionEstadoNoti < DATE_SUB(NOW(), INTERVAL 12 MINUTE);
            END;
            """)
            print("Procedimiento almacenado 'EliminarNotificaciones' creado o ya existe.")
            
            cursor.close()
        else:
            print("No se pudo conectar a la base de datos.")

    except Error as e:
        print(f"Error al intentar conectar o crear tablas: {e}")
    
    finally:
        if conexion.is_connected():
            conexion.close()
            print("Conexión cerrada.")

def mostrar_tablas():
    """Función para mostrar los registros de cada tabla creada"""
    try:
        conexion = mysql.connector.connect(
            host=host,
            user=usuario,
            password=contraseña,
            database=base_de_datos
        )
        
        if conexion.is_connected():
            cursor = conexion.cursor()
            tablas = ["actuaciones", "AUD_notificacion", "buscar_historico", 
                      "demanda", "historico", "notificacion", "usuarios"]
            
            for tabla in tablas:
                cursor.execute(f"SELECT * FROM {tabla}")
                registros = cursor.fetchall()
                
                print(f"\nContenido de la tabla '{tabla}':")
                if registros:
                    for registro in registros:
                        print(registro)
                else:
                    print("La tabla está vacía.")
            
            cursor.close()
        else:
            print("No se pudo conectar a la base de datos.")

    except Error as e:
        print(f"Error al intentar conectar o consultar las tablas: {e}")
    
    finally:
        if conexion.is_connected():
            conexion.close()
            print("Conexión cerrada.")

# Ejecutar la función de creación de tablas
conectar_y_crear_tablas()

# Ejecutar la función para mostrar el contenido de las tablas
mostrar_tablas()
