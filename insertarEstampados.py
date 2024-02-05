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





velazqueztciaBCI_ALZAMIENTO_DE_EMBARGO_REALIZADO = 20.000
velazqueztciaBCI_BUSQUEDA_POSITIVA = 30.000
velazqueztciaBCI_BUSQUEDAS_NEGATIVAS = 12.000
velazqueztciaBCI_NOT_PERSONAL = 90.000
velazqueztciaBCI_ART_44 = 30.000
velazqueztciaBCI_NOT_ART_52_CEDULA = 15.000
velazqueztciaBCI_NOT_TERCEROS = 15.000
velazqueztciaBCI_NOT_SENTENCIA = 15.000
velazqueztciaBCI_NOT_MARTILLERO = 15.000
velazqueztciaBCI_EMBARGO_FUERZA_PUBLICA_MUEB = 50.000
velazqueztciaBCI_EMBARGO_FRUSTRADO = 12.000
velazqueztciaBCI_EMBARGO_INMUEBLE = 35.000
velazqueztciaBCI_EMBARGO_VEHICULO_MAQ = 35.000
velazqueztciaBCI_NOT_TESORERIA_EMBARGO_IMPUESTOS = 20.000
velazqueztciaBCI_OPOSICION_RETIRO = 12.000
velazqueztciaBCI_RETIRO_ESPECIES = 50.000
velazqueztciaBCI_INCAUTACION_RETIRO_VEHICULO = 80.000
velazqueztciaBCI_RETIRO_ESPECIES_FRUSTRADO = 20.000
velazqueztciaBCI_GRUA_PROVINCIA_EMBARGO = 25.000
velazqueztciaBCI_GRUA_FUERA_PROVINCIA_ENC = 40.000

velazqueztciaITAU_BUSQUEDA_NEGATIVA = 22.222
velazqueztciaITAU_BUSQUEDA_POSITIVA = 33.333
velazqueztciaITAU_NOT_PER_MAYOR_4_MILLONES = 66.667
velazqueztciaITAU_NOT_PERS_CREDITO_GARANTIA = 66.667
velazqueztciaITAU_NOT_PER_MENOR_4_MILLONES = 55.556
velazqueztciaITAU_NOT_PER_OFICINA_RECPT = 27.778
velazqueztciaITAU_NOT_ART_44 = 50.000
velazqueztciaITAU_EMBARGO_FUERZA_PUBLICA = 61.111
velazqueztciaITAU_EMBARGO_VEHICULO = 33.333
velazqueztciaITAU_EMBARGO_PROPIEDAD = 38.889
velazqueztciaITAU_EMBARGO_TGR = 33.333
velazqueztciaITAU_EMBARGO_FRUSTRADO = 27.778
velazqueztciaITAU_ALZAMIENTO_EMB_PRECAUTORIA = 38.889
velazqueztciaITAU_NOTIFICACION_CBR = 22.222
velazqueztciaITAU_OPOCICION_RETIRO = 27.778
velazqueztciaITAU_RETIRO_FUERZA_PUBLICA = 66.667
velazqueztciaITAU_RETIRO_FRUSTRADO = 27.778
velazqueztciaITAU_NOT_MARTILLERO = 27.778
velazqueztciaITAU_NOT_ART_52 = 27.778
velazqueztciaITAU_NOT_VARIAS = 33.333
velazqueztciaITAU_NOT_ACREEDOR_HIPOT = 27.778
velazqueztciaITAU_DESCERRAJAMIENTO = 20.000
velazqueztciaITAU_FLETE_CAMION = 42.222
velazqueztciaITAU_FLETE_CAMION_FRUSTRADO = 16.667
velazqueztciaITAU_INCATACION_VEHICULO_LIVIANO_GRUA = 166.667
velazqueztciaITAU_INCAUTACION_VEHICULO_PESADO_GRUA = 166.667
velazqueztciaITAU_INVESTIGADOR_DOMICILIOS = 27.778
velazqueztciaITAU_TRAMITACION_EXORTOS = 55.556
velazqueztciaITAU_REQUERIMIENTO_PAGO = 5000
velazqueztciaITAU_OPOCICION_EMBARGO_BIENES_MUEBLES = 27.778
velazqueztciaITAU_INSCRIPCION_EMBARGO_CBR = 50.000
velazqueztciaITAU_INVESTIGADOR_BIENES = 80.000
velazqueztciaITAU_NOTIFICACION_AVISOS_DIARIO_OFICIAL = 1,111,111
velazqueztciaITAU_TRAMITACION_OFICIOS_OG_PUBLICOS = 5.556
velazqueztciaITAU_TRAMITACION_DOMINIO_CBR = 120.000

Aranceles_GLOVAL_BUSQUEDA_POSITIVA_AMBAS = 30.000
Aranceles_GLOVAL_NOT_ART_44_REQ_PAGO = 55.000
Aranceles_GLOVAL_BUSQUEDA_NEGATIVA = 23.000
Aranceles_GLOVAL_ALZAMIENTO_EMBARGO = 40.000
Aranceles_GLOVAL_EMBARGO_VEHICULO = 35.000
Aranceles_GLOVAL_NOT_MARTILLERO = 30.000
Aranceles_GLOVAL_NOT_PERSONAL_REQ_PAGO = 60.000
Aranceles_GLOVAL_NOT_CEDULA_ART_52 = 30.000
Aranceles_GLOVAL_RETIRO_FRUSTRADO = 30.000
Aranceles_GLOVAL_OP_RETIRO_BIENES_MUEBLES = 40.000
Aranceles_GLOVAL_INCAUTACION_VEHICULOS = 200.000
Aranceles_GLOVAL_RETIRO_ESPECIES_BIENES_MUEBLES = 70,000

Manuel_Aguirre_Abogados_BNCO_ESTADO_BUSQUEDA_NEGATIVA = 15.0000
Manuel_Aguirre_Abogados_BNCO_ESTADO_BUSQUEDA_POSITIVA = 15.000
Manuel_Aguirre_Abogados_BNCO_ESTADO_NOT_PERSONAL = 50.000
Manuel_Aguirre_Abogados_BNCO_ESTADO_NOT_ART_44 = 20.000
Manuel_Aguirre_Abogados_BNCO_ESTADO_REQUERIMIENTO_PAGO_EJECUTIVO = 10.000
Manuel_Aguirre_Abogados_BNCO_ESTADO_OP_EMBARGO = 10.000
Manuel_Aguirre_Abogados_BNCO_ESTADO_NOT_MARTILLERO = 25.000
Manuel_Aguirre_Abogados_BNCO_ESTADO_NOT_PERITO = 25.000
Manuel_Aguirre_Abogados_BNCO_ESTADO_NOT_CEDULA = 25.000
Manuel_Aguirre_Abogados_BNCO_ESTADO_NOT_CEDULA_TERCERO_AJENO = 25.000
Manuel_Aguirre_Abogados_BNCO_ESTADO_NOT_SENTENCIA = 25.000
Manuel_Aguirre_Abogados_BNCO_ESTADO_EMBARGO_BIENES_MUEBLES = 30.000
Manuel_Aguirre_Abogados_BNCO_ESTADO_EMBARGO_BIENES_MUEBLES_FUERZA_PUBLICA = 50.000
Manuel_Aguirre_Abogados_BNCO_ESTADO_EMBARGO_VEHICULO = 27.000


Olavarria_ABOGADOS_BUSQUEDA_POSITIVA = 30.000
Olavarria_ABOGADOS_BUSQUEDA_NEGATIVA = 14.000
Olavarria_ABOGADOS_NOT_PERSONAL_REQIERIMIENTO_PAGO = 50.000
Olavarria_ABOGADOS_NOT_REQUERIMIENTO_EJECUTIVO = 50.000
Olavarria_ABOGADOS_BUSQUEDAS_POSITIVAS_NOT_44_LEY_21394 = 60.000
Olavarria_ABOGADOS_OP_RETIRO = 15.000
Olavarria_ABOGADOS_NOT_SENTENCIA_MATILLERO_ACREEODRES_AUTO_PRUEBAS_CEDULA = 25.000

Agesa_BUSQUEDA_NEGATIVA = 36.000
Agesa_BUSQUEDA_POSITIVA = 42.000
Agesa_NOT_ART_44_REQ_PAGO_OP_EMBARGO = 54.000
Agesa_OP_RETIRO_VEHICULO = 48.000
Agesa_EMBARGO_FUERZA_PUBLICA = 60.000
Agesa_EMBARGO_FRUSTRADO = 42.000
Agesa_EMBARGO_PROPIEDAD = 48.000
Agesa_OP_EMBARGO = 36.000
Agesa_NOT_CEDULA = 36.000
Agesa_NOT_PERSONAL = 60.000
Agesa_NOT_SENTENCIA = 36.000
Agesa_NOT_AUTO_PRUEBA = 36.000
Agesa_NOT_MARTILLERO = 36.000
Agesa_NOT_CBR_EMBARGO_INMUEBLE = 48.000
Agesa_NOT_REG_NAC_VEHICULOS_MOT = 48.000
Agesa_EMBARGO_FUERZA_PUBLICA = 60.000
Agesa_LANZANAMIENTO_FUERTO_PUBLICA = 360.000
Agesa_INCAUTACION_VEHICULO = 360.000
Agesa_TRAMITACION_EXORTO = 2,6
Agesa_TRAMITACION_EXORTO_LEASING = 3,2
Agesa_ESCRITURA_ADJUDICACION = 96.000
Agesa_DACION_PAGO = 60.000
Agesa_AUTORIZACION_FIRMA = 1.800
Agesa_COPIAS_MANDATOS = 5.040
Agesa_DESARCHIVO_JUDICIAL = 6.000
Agesa_OFICIOS = 1.800
Agesa_MANDAMIENTOS = 1.800
Agesa_FOTOCOPIAS = 18.000
Agesa_EXHORTOS = 6.000
Agesa_NOT_AVISOS_PUBLICACION = 360.000
Agesa_PUBLICACION_REMATE = 360.000
Agesa_DOMICILIO_POSITIVO_REGION = 54.000
Agesa_DOMICILIO_POSITIVIO_FUERA_REGION = 60.000
Agesa_VEHICULOS_RNVM_ANNO_2000 = 24.000
Agesa_UBICACION_INMUEBLES_REGION = 42.000
Agesa_UBICACION_INMUEBLES_HIPOTECADO = 13.800
Agesa_UBICACION_INMUEBLES_FUERA_REGION = 48.000
Agesa_UBICACION_INMUEBLES_FUERA_REGION_HIPOTECADO = 15.840

Lautaro_Rosas_BUSQUEDA_NEGATIVA = 30.000
Lautaro_Rosas_BUSQUEDAS_POSITIVAS = 30.000
Lautaro_Rosas_NOT_DEMANDA_ART_44=30.000
Lautaro_Rosas_NOT_PERSONAL = 65.000
Lautaro_Rosas_REQ_PAGO_EJECUTIVO = 15.000
Lautaro_Rosas_OP_EMBARGO = 15.000
Lautaro_Rosas_NOT_MARTILLERO = 25.000
Lautaro_Rosas_NOT_PERITO = 30.000
Lautaro_Rosas_NOT_CEDULA = 30.000
Lautaro_Rosas_NOT_CEDULA_TERCERO_AJENO_JUICIO = 25.000
Lautaro_Rosas_NOT_SENTENCIA = 25.000
Lautaro_Rosas_EMBARGO_BIENES_MUEBLES_FUERZA_PUBLICA = 65.000
Lautaro_Rosas_EMBARGO_BIENES_MUEBLES = 35.000
Lautaro_Rosas_EMBARGO_VEHICULO = 30.000
Lautaro_Rosas_EMBARGO_FRUSTRADO = 30.000
Lautaro_Rosas_OP_RETIRO_ESPECIES = 20.000
Lautaro_Rosas_RETIRO_ESPECIES_FUERZA_PUBLICA = 100.000
Lautaro_Rosas_FLETE_RETIRO_ESPECIES = 200.000
Lautaro_Rosas_INCAUTACION_VEHICULOS_NEGATIVA = 100.000
Lautaro_Rosas_INCAUTACION_VEHICULO_POSITIVA = 300.000
Lautaro_Rosas_INSCRIPCION_EMBARGO_VEHICULO_RNVM = 30.000
Lautaro_Rosas_INCAUTACION_BIENES_NEGATIVA = 60.000
Lautaro_Rosas_NOT_ACREEDOR_HIP_SERVIU = 30.000
Lautaro_Rosas_REQ_PAGO_JUICIO_EJECUTIVO = 20.000
Lautaro_Rosas_NOT_DECRETO_REMATE = 30.000
Lautaro_Rosas_NOT_MEDIDA_PRECAUTORIA = 50.000
Lautaro_Rosas_INSCRIPCION_EMBARGO_BIENES_CBR = 35.000
Lautaro_Rosas_INSCRIPCION_MEDIDA_PREJUDICIAL_PRECAUTORIA = 50.000
Lautaro_Rosas_ALZAMIENTO_VEHICULOS = 40.000
Lautaro_Rosas_ALZAMIENTO_BIENES_INMUEBLES = 50.000


Santander_Natalia_LEGALIZACION_FIRMA = 2500
Santander_Natalia_EMBARGO_FRUSTRADO = 33.898
Santander_Natalia_NOT_MARTILLERO = 33.898
Santander_Natalia_OP_RETIRO = 33.989
Santander_Natalia_RET_ESPECIES = 45.198
Santander_Natalia_RET_ESPECIES_FLETE = 51.785
Santander_Natalia_RETIRO_ESPECIES_FUERZA_PUBLICA = 70.586
Santander_Natalia_NOT_PRUEBA_TESTIGO = 10.588
Santander_Natalia_GESTORIA_DACIONES = 50.000
Santander_Natalia_NOT_PERSONAL = 100.000
Santander_Natalia_NOT_CEDULA_ART_44 = 60.000
Santander_Natalia_NOT_CEDULA = 29.249
Santander_Natalia_OPOSICION_EMBARGO = 28249
Santander_Natalia_EMBARGO_PROPIEDAD = 33.750
Santander_Natalia_EMBARGO_FUERZA_PUBLICA = 67.997
Santander_Natalia_RETIRO_FRUSTRADO = 33.989
Santander_Natalia_HONORARIOS_EXORTO = 30.000
Santander_Natalia_DESARCHIVO = 11.299
Santander_Natalia_HIPOTECA_BANCO = 30.000
Santander_Natalia_BUSQUEDA_POSITIVA = 25.000
Santander_Natalia_BUSQUEDA_NEGATIVA = 22.599
Santander_Natalia_CONSERVADOR = 56.497
Santander_Natalia_GASTO_TASACION = 37.000
Santander_Natalia_COPIAS_AUTORIZADAS = 7.910
Santander_Natalia_CERTIFICADO_RVM = 1.130
Santander_Natalia_HONORARIOS_INCAUTADOR = 225.989
Santander_Natalia_INCAUTACION_RECEPTORA = 205.128
Santander_Natalia_BUSQUEDA_INVESTIGADOR = 28.249
Santander_Natalia_CERT_HIPOTECAS_GRAVAMENES = 22.599
Santander_Natalia_PUBLICACION = 385.000
Santander_Natalia_NOTARIA_ESCRITURA_ADJU = 395.480
Santander_Natalia_EMBARGO_VEHICULO = 39.548
Santander_Natalia_ALZAMIENTO_EMBARGO = 22.599
Santander_Natalia_PUBLICACION_PERMANENTE_DIARIO = 650.000
Santander_Natalia_INFO_SUMARIA_TESTIGOS = 44.444
Santander_Natalia_DEFENSOR_AUSENTE = 750.000
Santander_Natalia_CURADOR_HERENCIA_YACENTE = 750.000
Santander_Natalia_COMERCIAL = 1.600,000
Santander_Natalia_INSCRIPCION_DOMINIO_CONSERVADOR = 250.000
Santander_Natalia_PROCURADOR_NUMERO = 200.000
Santander_Natalia_GASTO_TASACION_PERICIAL = 1.468,927
Santander_Natalia_REQUERIMIENTO_PAGO = 5.085
Santander_Natalia_NOTARIA_DACION_PAGO = 169.942
Santander_Natalia_COPIA_ARCHIVO_JUDICIAL = 150.000
Santander_Natalia_VIGENCIA = 15.000
Santander_Natalia_COPIAS_AUTORIZADAS_EXPEDIENTE = 90.395
Santander_Natalia_DOMINIO_CBR = 3
Santander_Natalia_LANZAMIENTO_FUERZA_PUBLICA = 150.000
Santander_Natalia_ABSOLUCION_POSICIONES = 66.667
Santander_Natalia_PROPIEDAD = 106.000
Santander_Natalia_PRUEBA_TESTIMONIAL = 44.444
Santander_Natalia_ESCRITURA_NOTARIA_RESCILIACION = 150.000
Santander_Natalia_BVISTA_CAUSA = 15.000
Santander_Natalia_HIPOTECA = 33.333
Santander_Natalia_SUBROGACION_RETENCION = 25.000
Santander_Natalia_INSCRIPCION_EMBARGO_CRB = 00000
Santander_Natalia_AVALUO_VEHICULO_MAXIMO_TRES_MILLONES = 287.179
Santander_Natalia_AVALUO_VEHICULO_ENTRE_3_A_6_MILLONES = 338.462
Santander_Natalia_AVALUO_VEHICULO_ENTRE_6_A_8_MILLONES = 379487
Santander_Natalia_AVALUO_VEHICULO_MAS_8_MILLONES = 569.801
Santander_Natalia_VEHICULO_INCAUTADO_50_A_100_KMS = 68.376
Santander_Natalia_VEHICULO_INCAUTADO_101_A_150_KMS = 91.168
Santander_Natalia_VEHICULO_INCAUTADO_151_A_200_KMS = 136752
Santander_Natalia_VEHICULO_INCAUTADO_201_A_250_KMS = 170.940


HM_BANCO_Chile_BUSQUEDA_NEGATIVA = 15.000
HM_BANCO_Chile_BUSQUEDA_POSITIVA = 40.000
HM_BANCO_Chile_NOT_PERSONAL_MAYOR_4_MILLONES = 80.000
HM_BANCO_Chile_NOT_PERSONAL_MENOS_4_MILLONES = 60.000
HM_BANCO_Chile_NOT_PERSONAL_OFICINA_RECEPTOR = 30.000
HM_BANCO_Chile_NOT_ART_44 = 40.000
HM_BANCO_Chile_OP_EMBARGO = 15.000
HM_BANCO_Chile_EMBARGO_FUERZA_PUBLICA = 50.000
HM_BANCO_Chile_EMBARGO_VEHICULO = 30.000
HM_BANCO_Chile_EMBARGO_PROPIEDAD = 35.000
HM_BANCO_Chile_EMBARGO_TGR = 30.000
HM_BANCO_Chile_EMBARGO_FRUSTRADO = 25.000
HM_BANCO_Chile_OP_RETIRO = 25.000
HM_BANCO_Chile_RETIRO_FUERZA_PUBLICA = 60.000
HM_BANCO_Chile_RETIRO_FRUSTRADO = 30.000
HM_BANCO_Chile_NOT_REGISTRO_CIVIL = 25.000
HM_BANCO_ChileNOT_CBR = 30.000  
HM_BANCO_Chile_NOT_TGR = 25.000
HM_BANCO_Chile_NOT_MARTILLERO = 25.000
HM_BANCO_Chile_NOT_ART_52 = 25.000
HM_BANCO_Chile_NOT_VARIAS = 25.000
HM_BANCO_Chile_NOT_ACREEDOR_HIPOTECARIO = 25.000
HM_BANCO_Chile_DESCERRAJAMIENTO = 20.000
HM_BANCO_Chile_FLETE_CAMION = 50.000
HM_BANCO_Chile_FLETE_CAMION_FRUSTRADO = 20.000
HM_BANCO_Chile_INCAUTACION_VEHICULO_LIV = 300.000
HM_BANCO_Chile_INCAUTACION_VEHICULO_PESADO = 350.000

GMAC_hm_BUSQUEDA_NEGATIVA = 11.900
GMAC_hm_BUSQUEDA_POSITIVA = 14.875
GMAC_hm_EMBARGO_INSCRIPCION = 38.080
GMAC_hm_NOT_SENTENCIA_AUTO_PRUEBA = 29.750
GMAC_hm_NOT_ATR_44 = 52.360
GMAC_hm_NOT_PERSONAL_REQ_PAGO = 52.360
GMAC_hm_NOT_PERSONAL = 35.700
GMAC_hm_NOT_CEDULA = 29.750
GMAC_hm_OP_RETIRO = 26.180
GMAC_hm_TRAMITACION_EXHORTO_NOT = 47.600
GMAC_hm_ALZAMIENTO_EMBARGO_GMAC = 38.080
GMAC_hm_DESARCHIVO = 7140  