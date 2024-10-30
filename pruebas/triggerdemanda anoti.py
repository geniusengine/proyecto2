import mysql.connector
from mysql.connector import Error

# Datos de conexión
host = 'causas.mysql.database.azure.com'
usuario = 'admin_carlos'
contraseña = 'F14tomcat'
base_de_datos = 'matias1'

# Definición del código del trigger
trigger_sql = """
CREATE TRIGGER after_insert_demanda
AFTER INSERT ON demanda
FOR EACH ROW
BEGIN
    INSERT INTO notificacion (
        fechaNotificacion,
        numjui,
        nombTribunal,
        demandante,
        demandado,
        repre,
        mandante,
        domicilio,
        comuna,
        encargo,
        soli,
        arancel,
        estadoNoti,
        estadoCausa,
        actu
    )
    VALUES (
        NOW(),  -- Fecha de notificación actual
        NEW.numjui,
        NEW.nombTribunal,
        NEW.demandante,
        NEW.demandado,
        NEW.repre,
        NEW.mandante,
        NEW.domicilio,
        NEW.comuna,
        NEW.encargo,
        NEW.soli,
        NEW.arancel,
        0,  -- estadoNoti inicial
        0,  -- estadoCausa inicial
        NEW.actu
    );
END;
"""

def crear_trigger():
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
            # Ejecutar el código para crear el trigger
            cursor.execute(trigger_sql)
            print("Trigger 'after_insert_demanda' creado exitosamente.")
            cursor.close()
        else:
            print("No se pudo conectar a la base de datos.")

    except Error as e:
        print(f"Error al crear el trigger: {e}")

    finally:
        if conexion.is_connected():
            conexion.close()
            print("Conexión cerrada.")

# Ejecutar la función
crear_trigger()
