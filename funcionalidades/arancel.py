"""
 _______       _            _     _          ______        _                 _ 
(_______)     (_)       _  (_)   | |        (____  \      (_)               | |
 _______  ____ _  ___ _| |_ _  __| |_____    ____)  ) ____ _ _____ ____   __| |
|  ___  |/ ___) |/___|_   _) |/ _  | ___ |  |  __  ( / ___) (____ |  _ \ / _  |
| |   | | |   | |___ | | |_| ( (_| | ____|  | |__)  ) |   | / ___ | | | ( (_| |
|_|   |_|_|   |_(___/   \__)_|\____|_____)  |______/|_|   |_\_____|_| |_|\____|
    
Auteur: danie(danie.pro@gmail.com) 
arancel.py(Ɔ) 2024
Description : Saisissez la description puis « Tab »
Créé le :  mardi 6 février 2024 à 10:23:51 
Dernière modification : mardi 6 février 2024 à 12:45:16
"""

import sys
from PyQt6.QtWidgets import QDialog, QLabel, QLineEdit, QPushButton, QVBoxLayout, QComboBox, QMessageBox, QApplication

class ActualizarArancelDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Actualizar Arancel")
        self.layout = QVBoxLayout()
        # Create the first QComboBox for letters
        self.combo_letters = QComboBox()
        self.combo_letters.currentTextChanged.connect(self.update_number_combo_box)
        self.layout.addWidget(self.combo_letters)
        
        # Create the second QComboBox for numbers
        self.combo_numbers = QComboBox()
        self.combo_numbers.setEnabled(False)
        self.layout.addWidget(self.combo_numbers)
        

        self.btn_actualizar = QPushButton("Aceptar")
        self.btn_actualizar.clicked.connect(self.actualizar_arancel)
        self.layout.addWidget(self.btn_actualizar)

        self.setLayout(self.layout)

        
        # Create the first QComboBox for letters
        self.aranceles = {'velazqueztciaBCI_ALZAMIENTO_DE_EMBARGO_REALIZADO': '20.000', 
             'velazqueztciaBCI_BUSQUEDA_POSITIVA': '30.000',
             'velazqueztciaBCI_BUSQUEDAS_NEGATIVAS': '12.000',
             'velazqueztciaBCI_NOT_PERSONAL': '90.000', 
             'velazqueztciaBCI_ART_44': '30.000', 
             'velazqueztciaBCI_NOT_ART_52_CEDULA': '15.000',
             'velazqueztciaBCI_NOT_TERCEROS': '15.000', 
             'velazqueztciaBCI_NOT_SENTENCIA': '15.000', 
             'velazqueztciaBCI_NOT_MARTILLERO': '15.000', 
             'velazqueztciaBCI_EMBARGO_FUERZA_PUBLICA_MUEB': '50.000', 
             'velazqueztciaBCI_EMBARGO_FRUSTRADO': '12.000', 
             'velazqueztciaBCI_EMBARGO_INMUEBLE': '35.000', 
             'velazqueztciaBCI_EMBARGO_VEHICULO_MAQ': '35.000', 
             'velazqueztciaBCI_NOT_TESORERIA_EMBARGO_IMPUESTOS': '20.000', 
             'velazqueztciaBCI_OPOSICION_RETIRO': '12.000',
             'velazqueztciaBCI_RETIRO_ESPECIES': '50.000', 
             'velazqueztciaBCI_INCAUTACION_RETIRO_VEHICULO': '80.000', 
             'velazqueztciaBCI_RETIRO_ESPECIES_FRUSTRADO': '20.000', 
             'velazqueztciaBCI_GRUA_PROVINCIA_EMBARGO': '25.000', 
             'velazqueztciaBCI_GRUA_FUERA_PROVINCIA_ENC': '40.000',
             'velazqueztciaITAU_BUSQUEDA_NEGATIVA': '22.222', 
             'velazqueztciaITAU_BUSQUEDA_POSITIVA': '33.333', 
             'velazqueztciaITAU_NOT_PER_MAYOR_4_MILLONES': '66.667', 
             'velazqueztciaITAU_NOT_PERS_CREDITO_GARANTIA': '66.667', 
             'velazqueztciaITAU_NOT_PER_MENOR_4_MILLONES': '55.556',
             'velazqueztciaITAU_NOT_PER_OFICINA_RECPT': '27.778', 
             'velazqueztciaITAU_NOT_ART_44': '50.000', 
             'velazqueztciaITAU_EMBARGO_FUERZA_PUBLICA': '61.111',
             'velazqueztciaITAU_EMBARGO_VEHICULO': '33.333', 
             'velazqueztciaITAU_EMBARGO_PROPIEDAD': '38.889', 
             'velazqueztciaITAU_EMBARGO_TGR': '33.333', 
             'velazqueztciaITAU_EMBARGO_FRUSTRADO': '27.778', 
             'velazqueztciaITAU_ALZAMIENTO_EMB_PRECAUTORIA': '38.889', 
             'velazqueztciaITAU_NOTIFICACION_CBR': '22.222', 
             'velazqueztciaITAU_OPOCICION_RETIRO': '27.778', 
             'velazqueztciaITAU_RETIRO_FUERZA_PUBLICA': '66.667', 
             'velazqueztciaITAU_RETIRO_FRUSTRADO': '27.778',
             'velazqueztciaITAU_NOT_MARTILLERO': '27.778', 
             'velazqueztciaITAU_NOT_ART_52': '27.778', 
             'velazqueztciaITAU_NOT_VARIAS': '33.333', 
             'velazqueztciaITAU_NOT_ACREEDOR_HIPOT': '27.778', 
             'velazqueztciaITAU_DESCERRAJAMIENTO': '20.000', 
             'velazqueztciaITAU_FLETE_CAMION': '42.222', 
             'velazqueztciaITAU_FLETE_CAMION_FRUSTRADO': '16.667', 
             'velazqueztciaITAU_INCATACION_VEHICULO_LIVIANO_GRUA': '166.667', 
             'velazqueztciaITAU_INCAUTACION_VEHICULO_PESADO_GRUA': '166.667', 
             'velazqueztciaITAU_INVESTIGADOR_DOMICILIOS': '27.778', 
             'velazqueztciaITAU_TRAMITACION_EXORTOS': '55.556',
             'velazqueztciaITAU_OPOCICION_EMBARGO_BIENES_MUEBLES': '27.778', 
             'velazqueztciaITAU_INSCRIPCION_EMBARGO_CBR': '50.000', 
             'velazqueztciaITAU_INVESTIGADOR_BIENES': '80.000',
             'velazqueztciaITAU_TRAMITACION_OFICIOS_OG_PUBLICOS': '5.556',
             'velazqueztciaITAU_TRAMITACION_DOMINIO_CBR': '120.000', 
             'Aranceles_GLOVAL_BUSQUEDA_POSITIVA_AMBAS': '30.000',
             'Aranceles_GLOVAL_NOT_ART_44_REQ_PAGO': '55.000',
             'Aranceles_GLOVAL_BUSQUEDA_NEGATIVA': '23.000', 
             'Aranceles_GLOVAL_ALZAMIENTO_EMBARGO': '40.000',
             'Aranceles_GLOVAL_EMBARGO_VEHICULO': '35.000',
             'Aranceles_GLOVAL_NOT_MARTILLERO': '30.000', 
             'Aranceles_GLOVAL_NOT_PERSONAL_REQ_PAGO': '60.000', 
             'Aranceles_GLOVAL_NOT_CEDULA_ART_52': '30.000', 
             'Aranceles_GLOVAL_RETIRO_FRUSTRADO': '30.000', 
             'Aranceles_GLOVAL_OP_RETIRO_BIENES_MUEBLES': '40.000', 
             'Aranceles_GLOVAL_INCAUTACION_VEHICULOS': '200.000',
             'Manuel_Aguirre_Abogados_BNCO_ESTADO_BUSQUEDA_NEGATIVA': '15.000', 
             'Manuel_Aguirre_Abogados_BNCO_ESTADO_BUSQUEDA_POSITIVA': '15.000', 
             'Manuel_Aguirre_Abogados_BNCO_ESTADO_NOT_PERSONAL': '50.000', 
             'Manuel_Aguirre_Abogados_BNCO_ESTADO_NOT_ART_44': '20.000',
             'Manuel_Aguirre_Abogados_BNCO_ESTADO_REQUERIMIENTO_PAGO_EJECUTIVO': '10.000', 
             'Manuel_Aguirre_Abogados_BNCO_ESTADO_OP_EMBARGO': '10.000', 
             'Manuel_Aguirre_Abogados_BNCO_ESTADO_NOT_MARTILLERO': '25.000', 
             'Manuel_Aguirre_Abogados_BNCO_ESTADO_NOT_PERITO': '25.000', 
             'Manuel_Aguirre_Abogados_BNCO_ESTADO_NOT_CEDULA': '25.000', 
             'Manuel_Aguirre_Abogados_BNCO_ESTADO_NOT_CEDULA_TERCERO_AJENO': '25.000',
             'Manuel_Aguirre_Abogados_BNCO_ESTADO_NOT_SENTENCIA': '25.000', 
             'Manuel_Aguirre_Abogados_BNCO_ESTADO_EMBARGO_BIENES_MUEBLES': '30.000', 
             'Manuel_Aguirre_Abogados_BNCO_ESTADO_EMBARGO_BIENES_MUEBLES_FUERZA_PUBLICA': '50.000', 
             'Manuel_Aguirre_Abogados_BNCO_ESTADO_EMBARGO_VEHICULO': '27.000', 
             'Olavarria_ABOGADOS_BUSQUEDA_POSITIVA': '30.000', 
             'Olavarria_ABOGADOS_BUSQUEDA_NEGATIVA': '14.000', 
             'Olavarria_ABOGADOS_NOT_PERSONAL_REQIERIMIENTO_PAGO': '50.000',
             'Olavarria_ABOGADOS_NOT_REQUERIMIENTO_EJECUTIVO': '50.000', 
             'Olavarria_ABOGADOS_BUSQUEDAS_POSITIVAS_NOT_44_LEY_21394': '60.000', 
             'Olavarria_ABOGADOS_OP_RETIRO': '15.000', 
             'Olavarria_ABOGADOS_NOT_SENTENCIA_MATILLERO_ACREEODRES_AUTO_PRUEBAS_CEDULA': '25.000', 
             'Agesa_BUSQUEDA_NEGATIVA': '36.000', 
             'Agesa_BUSQUEDA_POSITIVA': '42.000', 
             'Agesa_NOT_ART_44_REQ_PAGO_OP_EMBARGO': '54.000', 
             'Agesa_OP_RETIRO_VEHICULO': '48.000',
             'Agesa_EMBARGO_FUERZA_PUBLICA': '60.000', 
             'Agesa_EMBARGO_FRUSTRADO': '42.000', 
             'Agesa_EMBARGO_PROPIEDAD': '48.000', 
             'Agesa_OP_EMBARGO': '36.000', 
             'Agesa_NOT_CEDULA': '36.000', 
             'Agesa_NOT_PERSONAL': '60.000', 
             'Agesa_NOT_SENTENCIA': '36.000',
             'Agesa_NOT_AUTO_PRUEBA': '36.000', 
             'Agesa_NOT_MARTILLERO': '36.000', 
             'Agesa_NOT_CBR_EMBARGO_INMUEBLE': '48.000',
             'Agesa_NOT_REG_NAC_VEHICULOS_MOT': '48.000',
             'Agesa_LANZANAMIENTO_FUERTO_PUBLICA': '360.000', 
             'Agesa_INCAUTACION_VEHICULO': '360.000', 
             'Agesa_ESCRITURA_ADJUDICACION': '96.000', 
             'Agesa_DACION_PAGO': '60.000',
             'Agesa_AUTORIZACION_FIRMA': '1.800', 
             'Agesa_COPIAS_MANDATOS': '5.040',
             'Agesa_DESARCHIVO_JUDICIAL': '6.000', 
             'Agesa_OFICIOS': '1.800',
             'Agesa_MANDAMIENTOS': '1.800', 
             'Agesa_FOTOCOPIAS': '18.000', 
             'Agesa_EXHORTOS': '6.000', 
             'Agesa_NOT_AVISOS_PUBLICACION': '360.000',
             'Agesa_PUBLICACION_REMATE': '360.000',
             'Agesa_DOMICILIO_POSITIVO_REGION': '54.000', 
             'Agesa_DOMICILIO_POSITIVIO_FUERA_REGION': '60.000', 
             'Agesa_VEHICULOS_RNVM_ANNO_2000': '24.000',
             'Agesa_UBICACION_INMUEBLES_REGION': '42.000',
             'Agesa_UBICACION_INMUEBLES_HIPOTECADO': '13.800',
             'Agesa_UBICACION_INMUEBLES_FUERA_REGION': '48.000',
             'Agesa_UBICACION_INMUEBLES_FUERA_REGION_HIPOTECADO': '15.840',
             'Lautaro_Rosas_BUSQUEDA_NEGATIVA': '30.000', 
             'Lautaro_Rosas_BUSQUEDAS_POSITIVAS': '30.000',
             'Lautaro_Rosas_NOT_DEMANDA_ART_44': '30.000', 
             'Lautaro_Rosas_NOT_PERSONAL': '65.000',
             'Lautaro_Rosas_REQ_PAGO_EJECUTIVO': '15.000', 
             'Lautaro_Rosas_OP_EMBARGO': '15.000', 
             'Lautaro_Rosas_NOT_MARTILLERO': '25.000',
             'Lautaro_Rosas_NOT_PERITO': '30.000', 
             'Lautaro_Rosas_NOT_CEDULA': '30.000',
             'Lautaro_Rosas_NOT_CEDULA_TERCERO_AJENO_JUICIO': '25.000',
             'Lautaro_Rosas_NOT_SENTENCIA': '25.000',
             'Lautaro_Rosas_EMBARGO_BIENES_MUEBLES_FUERZA_PUBLICA': '65.000',
             'Lautaro_Rosas_EMBARGO_BIENES_MUEBLES': '35.000',
             'Lautaro_Rosas_EMBARGO_VEHICULO': '30.000',
             'Lautaro_Rosas_EMBARGO_FRUSTRADO': '30.000', 
             'Lautaro_Rosas_OP_RETIRO_ESPECIES': '20.000',
             'Lautaro_Rosas_RETIRO_ESPECIES_FUERZA_PUBLICA': '100.000',
             'Lautaro_Rosas_FLETE_RETIRO_ESPECIES': '200.000', 
             'Lautaro_Rosas_INCAUTACION_VEHICULOS_NEGATIVA': '100.000',
             'Lautaro_Rosas_INCAUTACION_VEHICULO_POSITIVA': '300.000', 
             'Lautaro_Rosas_INSCRIPCION_EMBARGO_VEHICULO_RNVM': '30.000', 
             'Lautaro_Rosas_INCAUTACION_BIENES_NEGATIVA': '60.000', 
             'Lautaro_Rosas_NOT_ACREEDOR_HIP_SERVIU': '30.000', 
             'Lautaro_Rosas_REQ_PAGO_JUICIO_EJECUTIVO': '20.000',
             'Lautaro_Rosas_NOT_DECRETO_REMATE': '30.000', 
             'Lautaro_Rosas_NOT_MEDIDA_PRECAUTORIA': '50.000', 
             'Lautaro_Rosas_INSCRIPCION_EMBARGO_BIENES_CBR': '35.000',
             'Lautaro_Rosas_INSCRIPCION_MEDIDA_PREJUDICIAL_PRECAUTORIA': '50.000', 
             'Lautaro_Rosas_ALZAMIENTO_VEHICULOS': '40.000',
             'Lautaro_Rosas_ALZAMIENTO_BIENES_INMUEBLES': '50.000',
             'Santander_Natalia_EMBARGO_FRUSTRADO': '33.898', 
             'Santander_Natalia_NOT_MARTILLERO': '33.898',
             'Santander_Natalia_OP_RETIRO': '33.989', 
             'Santander_Natalia_RET_ESPECIES': '45.198',
             'Santander_Natalia_RET_ESPECIES_FLETE': '51.785',
             'Santander_Natalia_RETIRO_ESPECIES_FUERZA_PUBLICA': '70.586', 
             'Santander_Natalia_NOT_PRUEBA_TESTIGO': '10.588',
             'Santander_Natalia_GESTORIA_DACIONES': '50.000', 
             'Santander_Natalia_NOT_PERSONAL': '100.000', 
             'Santander_Natalia_NOT_CEDULA_ART_44': '60.000', 
             'Santander_Natalia_NOT_CEDULA': '29.249',
             'Santander_Natalia_EMBARGO_PROPIEDAD': '33.750', 
             'Santander_Natalia_EMBARGO_FUERZA_PUBLICA': '67.997', 
             'Santander_Natalia_RETIRO_FRUSTRADO': '33.989', 
             'Santander_Natalia_HONORARIOS_EXORTO': '30.000',
             'Santander_Natalia_DESARCHIVO': '11.299',
             'Santander_Natalia_HIPOTECA_BANCO': '30.000', 
             'Santander_Natalia_BUSQUEDA_POSITIVA': '25.000',
             'Santander_Natalia_BUSQUEDA_NEGATIVA': '22.599', 
             'Santander_Natalia_CONSERVADOR': '56.497', 
             'Santander_Natalia_GASTO_TASACION': '37.000',
             'Santander_Natalia_COPIAS_AUTORIZADAS': '7.910',
             'Santander_Natalia_CERTIFICADO_RVM': '1.130',
             'Santander_Natalia_HONORARIOS_INCAUTADOR': '225.989',
             'Santander_Natalia_INCAUTACION_RECEPTORA': '205.128',
             'Santander_Natalia_BUSQUEDA_INVESTIGADOR': '28.249', 
             'Santander_Natalia_CERT_HIPOTECAS_GRAVAMENES': '22.599', 
             'Santander_Natalia_PUBLICACION': '385.000',
             'Santander_Natalia_NOTARIA_ESCRITURA_ADJU': '395.480', 
             'Santander_Natalia_EMBARGO_VEHICULO': '39.548', 
             'Santander_Natalia_ALZAMIENTO_EMBARGO': '22.599',
             'Santander_Natalia_PUBLICACION_PERMANENTE_DIARIO': '650.000',
             'Santander_Natalia_INFO_SUMARIA_TESTIGOS': '44.444', 
             'Santander_Natalia_DEFENSOR_AUSENTE': '750.000', 
             'Santander_Natalia_CURADOR_HERENCIA_YACENTE': '750.000',
             'Santander_Natalia_COMERCIAL': '1.600', 
             'Santander_Natalia_INSCRIPCION_DOMINIO_CONSERVADOR': '250.000', 
             'Santander_Natalia_PROCURADOR_NUMERO': '200.000',
             'Santander_Natalia_GASTO_TASACION_PERICIAL': '1.468', 
             'Santander_Natalia_REQUERIMIENTO_PAGO': '5.085', 
             'Santander_Natalia_NOTARIA_DACION_PAGO': '169.942',
             'Santander_Natalia_COPIA_ARCHIVO_JUDICIAL': '150.000', 
             'Santander_Natalia_VIGENCIA': '15.000', 
             'Santander_Natalia_COPIAS_AUTORIZADAS_EXPEDIENTE': '90.395',
             'Santander_Natalia_LANZAMIENTO_FUERZA_PUBLICA': '150.000', 
             'Santander_Natalia_ABSOLUCION_POSICIONES': '66.667',
             'Santander_Natalia_PROPIEDAD': '106.000', 
             'Santander_Natalia_PRUEBA_TESTIMONIAL': '44.444', 
             'Santander_Natalia_ESCRITURA_NOTARIA_RESCILIACION': '150.000',
             'Santander_Natalia_BVISTA_CAUSA': '15.000', 
             'Santander_Natalia_HIPOTECA': '33.333',
             'Santander_Natalia_SUBROGACION_RETENCION': '25.000', 
             'Santander_Natalia_AVALUO_VEHICULO_MAXIMO_TRES_MILLONES': '287.179', 
             'Santander_Natalia_AVALUO_VEHICULO_ENTRE_3_A_6_MILLONES': '338.462', 
             'Santander_Natalia_AVALUO_VEHICULO_MAS_8_MILLONES': '569.801', 
             'Santander_Natalia_VEHICULO_INCAUTADO_50_A_100_KMS': '68.376',
             'Santander_Natalia_VEHICULO_INCAUTADO_101_A_150_KMS': '91.168', 
             'Santander_Natalia_VEHICULO_INCAUTADO_201_A_250_KMS': '170.940', 
             'HM_BANCO_Chile_BUSQUEDA_NEGATIVA': '15.000',
             'HM_BANCO_Chile_BUSQUEDA_POSITIVA': '40.000', 
             'HM_BANCO_Chile_NOT_PERSONAL_MAYOR_4_MILLONES': '80.000', 
             'HM_BANCO_Chile_NOT_PERSONAL_MENOS_4_MILLONES': '60.000',
             'HM_BANCO_Chile_NOT_PERSONAL_OFICINA_RECEPTOR': '30.000', 
             'HM_BANCO_Chile_NOT_ART_44': '40.000', 
             'HM_BANCO_Chile_OP_EMBARGO': '15.000',
             'HM_BANCO_Chile_EMBARGO_FUERZA_PUBLICA': '50.000', 
             'HM_BANCO_Chile_EMBARGO_VEHICULO': '30.000',
             'HM_BANCO_Chile_EMBARGO_PROPIEDAD': '35.000',
             'HM_BANCO_Chile_EMBARGO_TGR': '30.000',
             'HM_BANCO_Chile_EMBARGO_FRUSTRADO': '25.000',
             'HM_BANCO_Chile_OP_RETIRO': '25.000',
             'HM_BANCO_Chile_RETIRO_FUERZA_PUBLICA': '60.000',
             'HM_BANCO_Chile_RETIRO_FRUSTRADO': '30.000', 
             'HM_BANCO_Chile_NOT_REGISTRO_CIVIL': '25.000', 
             'HM_BANCO_ChileNOT_CBR': '30.000', 
             'HM_BANCO_Chile_NOT_TGR': '25.000', 
             'HM_BANCO_Chile_NOT_MARTILLERO': '25.000', 
             'HM_BANCO_Chile_NOT_ART_52': '25.000', 
             'HM_BANCO_Chile_NOT_VARIAS': '25.000',
             'HM_BANCO_Chile_NOT_ACREEDOR_HIPOTECARIO': '25.000',
             'HM_BANCO_Chile_DESCERRAJAMIENTO': '20.000', 
             'HM_BANCO_Chile_FLETE_CAMION': '50.000', 
             'HM_BANCO_Chile_FLETE_CAMION_FRUSTRADO': '20.000', 
             'HM_BANCO_Chile_INCAUTACION_VEHICULO_LIV': '300.000', 
             'HM_BANCO_Chile_INCAUTACION_VEHICULO_PESADO': '350.000',
             'GMAC_hm_BUSQUEDA_NEGATIVA': '11.900', 
             'GMAC_hm_BUSQUEDA_POSITIVA': '14.875',
             'GMAC_hm_EMBARGO_INSCRIPCION': '38.080', 
             'GMAC_hm_NOT_SENTENCIA_AUTO_PRUEBA': '29.750', 
             'GMAC_hm_NOT_ATR_44': '52.360', 
             'GMAC_hm_NOT_PERSONAL_REQ_PAGO': '52.360', 
             'GMAC_hm_NOT_PERSONAL': '35.700', 
             'GMAC_hm_NOT_CEDULA': '29.750', 
             'GMAC_hm_OP_RETIRO': '26.180',
             'GMAC_hm_TRAMITACION_EXHORTO_NOT': '47.600',
             'GMAC_hm_ALZAMIENTO_EMBARGO_GMAC': '38.080', 
             'LIDER_BCI_HM_BUSQUEDA_POSITIVA': '30.000', 
             'LIDER_BCI_HM_BUSQUEDA_NEGATIVA': '14.000', 
             'LIDER_BCI_HM_NOT_PERSONAL_REQUERIMIENTO': '50.000', 
             'LIDER_BCI_HM_NOT_REQUERIMIENTO_JUICIO_ART_44': '45.000', 
             'LIDER_BCI_HM_EMBARGO_INSC_BIEN_INMUEBLE': '55.000', 
             'LIDER_BCI_HM_EMBARGO_INSC_VEHICULO': '30.000',
             'LIDER_BCI_HM_DERECHO_INSC_VEHICULO': '4.300', 
             'LIDER_BCI_HM_ALZAMIENTO_EMBARGO': '30.000', 
             'LIDER_BCI_HM_OP_RETIRO': '15.000', 
             'LIDER_BCI_HM_OP_EMBARGO_OTROS_BIENESINM': '15.000', 
             'LIDER_BCI_HM_NOT_SENTENCIA_NOT_MARTILLERO_OTROS': '25.000', 
             'LIDER_BCI_HM_NOT_REQUERIMIENTO_TRABA_EMB': '190.000', 
             'LIDER_BCI_HM_RETIRO_VEHICULO': '170.000',
             'LIDER_BCI_HM_RET_FRUSTRADO_VEHICULO': '15.000',
             'LIDER_BCI_HM_RET_FUERZA_PUBLICA_OTROS_BIENES': '50.000', 
             'LIDER_BCI_HM_EMB_OTROS_BIENES_FUERZA_PUB': '40.000', 
             'LIDER_BCI_HM_EMB_FRUSTRADO_BIENESM': '15.000', 
             'LIDER_BCI_HM_DEMANDA_800MIL': '166.667', 
             'LIDER_BCI_HM_DEMANDA_1MILLON_A_3MILLONES': '277.000', 
             'LIDER_BCI_HM_DEMANDA_3MILLONES_EN_ADELANTE': '322.000', 
             'LIDER_BCI_HM_INV_DOMICILIO_BUSQUEDA_POSITIVA': '50.000', 
             'LIDER_BCI_HM_INV_EMBARGAR_RESULTADO_POSITIVO_HEREDERO': '50.000',
             'LIDER_BCI_HM_INV_CTA_CTE_SALDO_POSITIVO': '20.000', 
             'LIDER_BCI_HM_AUT_REMATES_REGIONES': '60.000', 
             'LIDER_BCI_HM_TRAMITACION_OFICIO': '30.000', 
             'LIDER_BCI_HM_CONFF_EXHORTO': '3.000', 
             'LIDER_BCI_HM_CONF_OFICIO': '3.000', 
             'LIDER_BCI_HM_TRAMITACION_EXHORTO_REGIONES': '44.444', 
             'LIDER_BCI_HM_TRAMITACION_MELIPILLA_BUIN_PENAFLOR': '20.000', 
             'LIDER_BCI_HM_DESARCHIVO_CARTERA_REEMBOLSO': '6.000', 
             'LIDER_BCI_HM_CAV_NUEVAS_ASIGNACIONES': '1.000', 
             'CAJA_LOS_ANDES_BUSQUEDA_NEGATIVA': '12.000', 
             'CAJA_LOS_ANDES_BUSQUEDA_POSITIVA': '30.000', 
             'CAJA_LOS_ANDES_NOT_PERSONAL_REQ_EMBARGO': '70.000', 
             'CAJA_LOS_ANDES_NOT_PERSONAL_REQ_OPOSICION': '70.000',
             'CAJA_LOS_ANDES_EMBARGO_FUERZA_PUBLICA': '58.000', 
             'CAJA_LOS_ANDES_NOT_PERSONAL_REQ_PAGO': '35.000', 
             'CAJA_LOS_ANDES_NOT_ART_44': '30.000',
             'CAJA_LOS_ANDES_NOTIFICACION_MARTILLERO': '20.000',
             'CAJA_LOS_ANDES_NOT_CEDULA_ART_52': '16.000',
             'CAJA_LOS_ANDES_NOT_AVISO_PUB_REMATE': '20.000', 
             'CAJA_LOS_ANDES_OP_FISICA_EMBARGO': '15.000', 
             'CAJA_LOS_ANDES_OP_RETIRO_ESPECIES': '15.000', 
             'CAJA_LOS_ANDES_EMB_VEHICULO_RNVM': '30.000', 
             'CAJA_LOS_ANDES_EMB_BIEN_RAIZ_CBR': '25.000', 
             'CAJA_LOS_ANDES_EMB_VALORES_CTA_CTE': '28.000',
             'CAJA_LOS_ANDES_EMB_FRUSTRADO': '30.000', 
             'CAJA_LOS_ANDES_RETIRO_FRUSTRADO': '20.000', 
             'CAJA_LOS_ANDES_RETIRO_VEHICULO': '120.000', 
             'CAJA_LOS_ANDES_RETIRO_ESPECIES_FZA_PUBLICA': '40.000', 
             'CAJA_LOS_ANDES_ABSOLUCION_POSICIONES': '25.000', 
             'CAJA_LOS_ANDES_PRUEBA_CONFESIONAL_TESTIMONIAL': '30.000', 
             'CAJA_LOS_ANDES_ALZAMIENTO_EMBARGO': '30.000', 
             'TANNER_BUSQUEDA_NEGATIVA': '22.759', 
             'TANNER_BUSQUEDA_NEGATIVA_AVAL': '22.759', 
             'TANNER_BUSQUEDA_POSITIVA': '40.759', 
             'TANNER_BUSQUEDA_POSITIVA_AVAL': '40.759', 
             'TANNER_NOT_PERSONAL': '62.069', 
             'TANNER_NOT_PERSONAL_AVAL': '62.069',
             'TANNER_NOT_ART_44': '51.724',
             'TANNER_NOT_ART_33_AVAL': '41.724', 
             'TANNER_NOT_CEDULA_SENTENCIA': '25.862', 
             'TANNER_NOT_CEDULA_MARTILLERO': '25.862', 
             'TANNER_NOT_CEDULA_TERCEROS': '25.862', 
             'TANNER_EMBARGO_INSCRIPCION_CBR': '65.172', 
             'TANNER_EMBARGO_VEHICULO': '45.287', 
             'TANNER_OTROS_EMBARGOS': '56.897', 
             'TANNER_RETIRO_BIENES_MUEBLES_GASTOS': '56.897', 
             'TANNER_OP_RET_MUEBLES': '15.517', 
             'TANNER_OP_RET_VEHICULO': '30.259', 
             'TANNER_INCAUTACION_VEHICULO_10MM': '230.000',
             'TANNER_INCAUTACION_VEHICULO': '226.436',
             'TANNER_EMBARGO_FRUSTRADO': '15.517',
             'TANNER_RETIRO_FRUSTRADO': '34.138', 
             'TANNER_DISTANCIA_COMUNA_PTEALTO_PADREHURT': '11.322', 
             'TANNER_DISTANCIA_SANMIGUEL': '9.057', 
             'TANNER_ALZAMIENTO_EMBARGO': '31.034',
             'LOPEZ_SA_BUSQUEDA_NEGATIVA': '12.000',
             'LOPEZ_SA_BUSQUEDA_POSITIVA': '15.000', 
             'LOPEZ_SA_NOT_REQUERIMIENTO_OP': '34.000',
             'LOPEZ_SA_NOT_ART_44': '22.000', 
             'LOPEZ_SA_EMBARGO_POSITIVO_FZA_PUBLICA': '28.000', 
             'LOPEZ_SA_EMBARGO_FRUSTRADO': '24.000', 
             'LOPEZ_SA_NOT_MARTILLERO': '22.000', 
             'LOPEZ_SA_OP_RETIRO_ESPECIES': '10.000', 
             'LOPEZ_SA_RET_POSITIVO': '30.000',
             'LOPEZ_SA_RET_NEGATIVO': '20.000', 
             'LOPEZ_SA_NOT_ARRESTO': '15.000', 
             'LOPEZ_SA_NOT_ART_52': '15.000', 
             'ELVEN_ASESORIAS_BUSQUEDA_POSITIVA': '10.000', 
             'ELVEN_ASESORIAS_BUSQUEDA_NEGATIVA': '8.000', 
             'ELVEN_ASESORIAS_NOT_CEDULA_OP_EMBARGO': '16.000', 
             'ELVEN_ASESORIAS_NOT_PERS_OP_EMBARGO': '26.000',
             'ELVEN_ASESORIAS_EMBARGO_POSITIVO': '35.000', 
             'ELVEN_ASESORIAS_EMBARGO_NEGATIVO': '15.000', 
             'ELVEN_ASESORIAS_EMBARGO_POSITIVO_CTA_CTE': '26.000', 
             'ELVEN_ASESORIAS_EMBARGO_NEGATIVO_CTA_CTE': '15.000', 
             'ELVEN_ASESORIAS_NOT_MARTILLERO': '15.000', 
             'ELVEN_ASESORIAS_OP_RETIRO': '15.000', 
             'ELVEN_ASESORIAS_NOT_ART_52': '8.000', 
             'ELVEN_ASESORIAS_RET_ESPECIES_FRUSTRADO': '15.000', 
             'ELVEN_ASESORIAS_RET_ESPECIES_POSITIVO': '35.000', 
             'SOCOFIN_BUSQUEDA_NEGATIVA': '15.000', 
             'SOCOFIN_BUSQUEDA_POSITIVA': '40.000', 
             'SOCOFIN_NOT_PERSONAL_MAYOR_4MILLONES': '60.000', 
             'SOCOFIN_NOT_PERSONAL_GARANTIA': '60.000', 
             'SOCOFIN_NOT_PERSONAL_MENOR_4MILLONES': '50.000',
             'SOCOFIN_NOT_PERSONAL_RECEPTOR': '25.000',
             'SOCOFIN_NOT_ART_44_CPC': '50.000', 
             'SOCOFIN_OP_EMBARGO': '5.000', 
             'SOCOFIN_EMBARGO_FUERZA_PUBLICA': '45.000', 
             'SOCOFIN_EMBARGO_VEHICULO': '20.000', 
             'SOCOFIN_EMBARGO_PROPIEDAD': '50.000', 
             'SOCOFIN_EMBARGO_TESORERIA': '20.000', 
             'SOCOFIN_EMBARGO_RNVM': '18.000', 
             'SOCOFIN_NOT_CBR': '18.000', 
             'SOCOFIN_NOT_TESORERIA': '18.000', 
             'SOCOFIN_EMBARGO_FRUSTRADO': '15.000', 
             'SOCOFIN_OP_RETIRO': '15.000', 
             'SOCOFIN_RET_FUERZA_PUBLICA': '50.000', 
             'SOCOFIN_RET_FRUSTRADO': '20.000', 
             'SOCOFIN_NOT_MARTILLERO': '18.000', 
             'SOCOFIN_NOT_ART_52': '18.000', 
             'SOCOFIN_NOT_VARIAS': '18.000', 
             'SOCOFIN_NOT_ACREEDOR_HIPOTECARIO': '18.000', 
             'SOCOFIN_DESCERRAJAMIENTO': '10.000', 
             'SOCOFIN_FLETE_CAMION': '30.000', 
             'SOCOFIN_INCAUTACION_VEHICULO_LIVIANO': '250.000', 
             'SOCOFIN_INCAUTACION_VEHICULO_PESADO': '350.000',
             'ORPRO_BUSQUEDA_NEGATIVA': '10.500', 
             'ORPRO_BUSQUEDA_POSITIVA': '9.000',
             'ORPRO_NOT_PERSONAL_OP': '25.000', 
             'ORPRO_NOT_PERSONAL_EMBARGO': '32.000', 
             'ORPRO_NOT_ART_44_OP': '30.000', 
             'ORPRO_EMBARGO_FUERZA_PUBLICA': '20.000',
             'ORPRO_EMBARGO_FRUSTRADO_FUERZA_PUB': '15.000', 
             'ORPRO_NOT_MARTILLERO': '15.000',
             'ORPRO_OP_RETIRO_ESPECIES': '6.000',
             'ORPRO_RET_ESPECIES': '30.000',
             'ORPRO_RET_FRUSTRADO': '15.000',
             'ORPRO_NOT_ARRESTO': '15.000', 
             'ORPRO_NOT_ART_52': '16.000', 
             'ORPRO_NOT_CEDULA': '16.000', 
             'ORPRO_NOT_EMBARGO_BIEN_RAIZ': '20.000', 
             'ORPRO_NOT_REGISTRO_CIVIL': '20.000'}


        # Luego, puedes agregar las opciones al QComboBox
# Llenar el QComboBox con las opciones
        for opcion, arancel in self.aranceles.items():
            self.combo_letters.addItem(opcion)

# 
    def update_number_combo_box(self, selected_letter):
        self.combo_numbers.clear()
        arancel = self.aranceles.get(selected_letter)
        if arancel:
            self.combo_numbers.addItem(arancel)
            self.combo_numbers.setEnabled(True)
        else:
            self.combo_numbers.setEnabled(False)

    def actualizar_arancel(self):
        # Get the selected values from combo boxes
        selected_letter = self.combo_letters.currentText()
        selected_number = self.combo_numbers.currentText()

        # Combine the selected values (you may adjust the format based on your needs)
        new_arancel_value = f"{selected_letter}-{selected_number}"

        # Assume you have access to the table widget in the parent, replace 'table' with your actual table widget
        selected_row = self.parent().table.currentRow()

        # Check if a row is selected
        if selected_row != -1:
            # Update the 'arancel' column in the selected row with the new value
            self.parent().table.setItem(selected_row, 1, QTableWidgetItem(new_arancel_value))

            # You may want to trigger any additional logic here based on the new value


def main():
        app = QApplication(sys.argv)
        window = ActualizarArancelDialog()

        window.show()
        sys.exit(app.exec())

if __name__ == '__main__':
        main()
