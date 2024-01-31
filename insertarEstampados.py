import inspect

# Obtiene el nombre del script actual
nombre_script = inspect.getfile(inspect.currentframe())

while True:
    # Solicita al usuario que ingrese el mandante, el estampado y el precio
    mandante = input("Por favor, ingrese el mandante (o 'stop' para terminar): ")
    
    # Si el usuario ingresó 'stop', termina el bucle
    if mandante.lower() == 'stop':
        break

    estampado = input("Por favor, ingrese el estampado: ")
    precio = input("Por favor, ingrese el precio: ")

    # Crea el nombre de la variable a partir del mandante y el estampado
    nombre_variable = f"{mandante}_{estampado}"

    # Crea el contenido del archivo
    contenido = f"\n{nombre_variable} = {precio}"

    # Abre el archivo en modo de agregar ('a') y escribe el contenido
    with open(nombre_script, 'a') as f:
        f.write(contenido)




