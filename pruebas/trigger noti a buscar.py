import mysql.connector
from mysql.connector import Error

# Datos de conexión
host = 'causas.mysql.database.azure.com'
usuario = 'admin_carlos'
contraseña = 'F14tomcat'
base_de_datos = 'matias1'

# Definición del código del trigger
trigger_sql = """
CREATE TRIGGER after_delete_notificacion_buscar_historia
BEFORE DELETE ON notificacion
FOR EACH ROW
BEGIN
    IF OLD.estadoNoti = 1 AND OLD.estadoCausa = 1 THEN
        INSERT INTO buscar_historico (
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
            OLD.fechaNotificacion,
            OLD.numjui,
            OLD.nombTribunal,
            OLD.demandante,
            OLD.demandado,
            OLD.repre,
            OLD.mandante,
            OLD.domicilio,
            OLD.comuna,
            OLD.encargo,
            OLD.soli,
            OLD.arancel,
            OLD.estadoNoti,
            OLD.estadoCausa,
            OLD.actu
        );
    END IF;
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
            print("Trigger 'after_delete_notificacion' creado exitosamente.")
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
