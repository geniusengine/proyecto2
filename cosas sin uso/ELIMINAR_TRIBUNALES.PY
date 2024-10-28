import pymssql

def eliminar_datos():
    # Solicitar al usuario que ingrese el nombre del tribunal a eliminar
    nombTribunal = input("Por favor, ingrese el nombre del tribunal a eliminar (o 'close' para salir): ")

    while nombTribunal.lower() != 'close':
        # Establecer la conexión con la base de datos
        db_connection = pymssql.connect(
            server='vps-3697915-x.dattaweb.com',
            user='daniel',
            password='LOLxdsas--',
            database='micau5a'
        )

        try:
            # Crear un cursor
            cursor = db_connection.cursor()

            # Definir la consulta de eliminación
            delete_query = "DELETE FROM [dbo].[tribunal] WHERE [nombTribunal] = %s"

            # Ejecutar la consulta de eliminación
            cursor.execute(delete_query, (nombTribunal,))

            # Confirmar la transacción
            db_connection.commit()

        except Exception as e:
            # Si ocurre un error, imprimirlo y revertir la transacción
            print(e)
            db_connection.rollback()

        finally:
            # Cerrar la conexión con la base de datos
            db_connection.close()

        # Solicitar al usuario que ingrese el nombre del tribunal a eliminar
        nombTribunal = input("Por favor, ingrese el nombre del tribunal a eliminar (o 'close' para salir): ")

# Ejemplo de uso:
eliminar_datos()