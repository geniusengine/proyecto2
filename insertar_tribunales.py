import pymssql

def insertar_datos():
    while True:
        # Solicitar al usuario que ingrese el nombre del tribunal
        nombTribunal = input("Por favor, ingrese el nombre del tribunal (o 'close' para salir): ")

        # Si el usuario ingresa 'close', salir del bucle
        if nombTribunal.lower() == 'close':
            break

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

            # Definir la consulta de inserción
            insert_query = "INSERT INTO [dbo].[tribunal] ([nombTribunal]) VALUES (%s)"

            # Ejecutar la consulta de inserción
            cursor.execute(insert_query, (nombTribunal,))

            # Confirmar la transacción
            db_connection.commit()

        except Exception as e:
            # Si ocurre un error, imprimirlo y revertir la transacción
            print(e)
            db_connection.rollback()

        finally:
            # Cerrar la conexión con la base de datos
            db_connection.close()

# Ejemplo de uso:
insertar_datos()