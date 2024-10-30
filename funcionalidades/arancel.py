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
Dernière modification : mercredi 7 février 2024 à 16:57:09
"""

import sys
from PyQt6.QtWidgets import QDialog, QLabel, QLineEdit, QPushButton, QVBoxLayout, QComboBox, QMessageBox, QApplication
from PyQt6.QtCore import pyqtSignal
import mysql.connector
import logging
from datetime import datetime

class ActualizarArancelDialog(QDialog):
    def __init__(self, fechaNotificacion, numjui, nombTribunal, demandante, demandado, repre, mandante, domicilio, comuna, encargo, soli, arancel, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Actualizar Arancel")
        self.layout = QVBoxLayout()

        # Crear el primer QComboBox para las letras
        self.combo_letters = QComboBox()
        self.combo_letters.currentTextChanged.connect(self.update_number_combo_box)
        self.layout.addWidget(self.combo_letters)
       
        # Crear el segundo QComboBox para los números
        self.combo_numbers = QComboBox()
        self.combo_numbers.setEnabled(False)
        self.layout.addWidget(self.combo_numbers)

        self.btn_actualizar = QPushButton("Aceptar")
        self.btn_actualizar.clicked.connect(lambda: self.actualizar_tabla(arancel_value=arancel))
        self.layout.addWidget(self.btn_actualizar)

        self.setLayout(self.layout)

        # Guardar los datos recibidos
        self.fechaNotificacion = fechaNotificacion
        self.numjui = numjui
        self.nombTribunal = nombTribunal
        self.demandante = demandante
        self.demandado = demandado
        self.repre = repre
        self.mandante = mandante
        self.domicilio = domicilio
        self.comuna = comuna
        self.encargo = encargo
        self.soli = soli
        self.arancel = arancel

        self.selected_item = None
        self.combo_letters.currentIndexChanged.connect(self.on_combo_letters_changed)

        # Lista de aranceles
        self.aranceles = {'velazqueztciaBCI_ALZAMIENTO_DE_EMBARGO_REALIZADO': '20000',
             'velazqueztciaBCI_BUSQUEDA_POSITIVA': '30000',
             'velazqueztciaBCI_BUSQUEDAS_NEGATIVAS': '12000',
             'velazqueztciaBCI_NOT_PERSONAL': '90000', 
             'velazqueztciaBCI_ART_44': '30000', 
             'velazqueztciaBCI_NOT_ART_52_CEDULA': '15000',
             'velazqueztciaBCI_NOT_TERCEROS': '15000', 
             'velazqueztciaBCI_NOT_SENTENCIA': '15000', 
             'velazqueztciaBCI_NOT_MARTILLERO': '15000', 
             'velazqueztciaBCI_EMBARGO_FUERZA_PUBLICA_MUEB': '50000', 
             'velazqueztciaBCI_EMBARGO_FRUSTRADO': '12000', 
             'velazqueztciaBCI_EMBARGO_INMUEBLE': '35000', 
             'velazqueztciaBCI_EMBARGO_VEHICULO_MAQ': '35000', 
             'velazqueztciaBCI_NOT_TESORERIA_EMBARGO_IMPUESTOS': '20000', 
             'velazqueztciaBCI_OPOSICION_RETIRO': '12000',
             'velazqueztciaBCI_RETIRO_ESPECIES': '50000', 
             'velazqueztciaBCI_INCAUTACION_RETIRO_VEHICULO': '80000', 
             'velazqueztciaBCI_RETIRO_ESPECIES_FRUSTRADO': '20000', 
             'velazqueztciaBCI_GRUA_PROVINCIA_EMBARGO': '25000', 
             'velazqueztciaBCI_GRUA_FUERA_PROVINCIA_ENC': '40000',
             'velazqueztciaITAU_BUSQUEDA_NEGATIVA': '22222', 
             'velazqueztciaITAU_BUSQUEDA_POSITIVA': '33333', 
             'velazqueztciaITAU_NOT_PER_MAYOR_4_MILLONES': '66667', 
             'velazqueztciaITAU_NOT_PERS_CREDITO_GARANTIA': '66667', 
             'velazqueztciaITAU_NOT_PER_MENOR_4_MILLONES': '55556',
             'velazqueztciaITAU_NOT_PER_OFICINA_RECPT': '27778', 
             'velazqueztciaITAU_NOT_ART_44': '50000', 
             'velazqueztciaITAU_EMBARGO_FUERZA_PUBLICA': '61111',
             'velazqueztciaITAU_EMBARGO_VEHICULO': '33333', 
             'velazqueztciaITAU_EMBARGO_PROPIEDAD': '38889', 
             'velazqueztciaITAU_EMBARGO_TGR': '33333', 
             'velazqueztciaITAU_EMBARGO_FRUSTRADO': '27778', 
             'velazqueztciaITAU_ALZAMIENTO_EMB_PRECAUTORIA': '38889', 
             'velazqueztciaITAU_NOTIFICACION_CBR': '22222', 
             'velazqueztciaITAU_OPOCICION_RETIRO': '27778', 
             'velazqueztciaITAU_RETIRO_FUERZA_PUBLICA': '66667', 
             'velazqueztciaITAU_RETIRO_FRUSTRADO': '27778',
             'velazqueztciaITAU_NOT_MARTILLERO': '27778', 
             'velazqueztciaITAU_NOT_ART_52': '27778', 
             'velazqueztciaITAU_NOT_VARIAS': '33333', 
             'velazqueztciaITAU_NOT_ACREEDOR_HIPOT': '27778', 
             'velazqueztciaITAU_DESCERRAJAMIENTO': '20000', 
             'velazqueztciaITAU_FLETE_CAMION': '42222', 
             'velazqueztciaITAU_FLETE_CAMION_FRUSTRADO': '16667', 
             'velazqueztciaITAU_INCATACION_VEHICULO_LIVIANO_GRUA': '166667', 
             'velazqueztciaITAU_INCAUTACION_VEHICULO_PESADO_GRUA': '166667', 
             'velazqueztciaITAU_INVESTIGADOR_DOMICILIOS': '27778', 
             'velazqueztciaITAU_TRAMITACION_EXORTOS': '55556',
             'velazqueztciaITAU_OPOCICION_EMBARGO_BIENES_MUEBLES': '27778', 
             'velazqueztciaITAU_INSCRIPCION_EMBARGO_CBR': '50000', 
             'velazqueztciaITAU_INVESTIGADOR_BIENES': '80000',
             'velazqueztciaITAU_TRAMITACION_OFICIOS_OG_PUBLICOS': '5556',
             'velazqueztciaITAU_TRAMITACION_DOMINIO_CBR': '120000', 
             'Aranceles_GLOVAL_BUSQUEDA_POSITIVA_AMBAS': '30000',
             'Aranceles_GLOVAL_NOT_ART_44_REQ_PAGO': '55000',
             'Aranceles_GLOVAL_BUSQUEDA_NEGATIVA': '23000', 
             'Aranceles_GLOVAL_ALZAMIENTO_EMBARGO': '40000',
             'Aranceles_GLOVAL_EMBARGO_VEHICULO': '35000',
             'Aranceles_GLOVAL_NOT_MARTILLERO': '30000', 
             'Aranceles_GLOVAL_NOT_PERSONAL_REQ_PAGO': '60000', 
             'Aranceles_GLOVAL_NOT_CEDULA_ART_52': '30000', 
             'Aranceles_GLOVAL_RETIRO_FRUSTRADO': '30000', 
             'Aranceles_GLOVAL_OP_RETIRO_BIENES_MUEBLES': '40000', 
             'Aranceles_GLOVAL_INCAUTACION_VEHICULOS': '200000',
             'Manuel_Aguirre_Abogados_BNCO_ESTADO_BUSQUEDA_NEGATIVA': '15000', 
             'Manuel_Aguirre_Abogados_BNCO_ESTADO_BUSQUEDA_POSITIVA': '15000', 
             'Manuel_Aguirre_Abogados_BNCO_ESTADO_NOT_PERSONAL': '50000', 
             'Manuel_Aguirre_Abogados_BNCO_ESTADO_NOT_ART_44': '20000',
             'Manuel_Aguirre_Abogados_BNCO_ESTADO_REQUERIMIENTO_PAGO_EJECUTIVO': '10000', 
             'Manuel_Aguirre_Abogados_BNCO_ESTADO_OP_EMBARGO': '10000', 
             'Manuel_Aguirre_Abogados_BNCO_ESTADO_NOT_MARTILLERO': '25.000', 
             'Manuel_Aguirre_Abogados_BNCO_ESTADO_NOT_PERITO': '25000', 
             'Manuel_Aguirre_Abogados_BNCO_ESTADO_NOT_CEDULA': '25000', 
             'Manuel_Aguirre_Abogados_BNCO_ESTADO_NOT_CEDULA_TERCERO_AJENO': '25000',
             'Manuel_Aguirre_Abogados_BNCO_ESTADO_NOT_SENTENCIA': '25000', 
             'Manuel_Aguirre_Abogados_BNCO_ESTADO_EMBARGO_BIENES_MUEBLES': '30000', 
             'Manuel_Aguirre_Abogados_BNCO_ESTADO_EMBARGO_BIENES_MUEBLES_FUERZA_PUBLICA': '50000', 
             'Manuel_Aguirre_Abogados_BNCO_ESTADO_EMBARGO_VEHICULO': '27000', 
             'Olavarria_ABOGADOS_BUSQUEDA_POSITIVA': '30000', 
             'Olavarria_ABOGADOS_BUSQUEDA_NEGATIVA': '14000', 
             'Olavarria_ABOGADOS_NOT_PERSONAL_REQIERIMIENTO_PAGO': '50000',
             'Olavarria_ABOGADOS_NOT_REQUERIMIENTO_EJECUTIVO': '50000', 
             'Olavarria_ABOGADOS_BUSQUEDAS_POSITIVAS_NOT_44_LEY_21394': '60000', 
             'Olavarria_ABOGADOS_OP_RETIRO': '15000', 
             'Olavarria_ABOGADOS_NOT_SENTENCIA_MATILLERO_ACREEODRES_AUTO_PRUEBAS_CEDULA': '25000', 
             'Agesa_BUSQUEDA_NEGATIVA': '36000', 
             'Agesa_BUSQUEDA_POSITIVA': '42000', 
             'Agesa_NOT_ART_44_REQ_PAGO_OP_EMBARGO': '54000', 
             'Agesa_OP_RETIRO_VEHICULO': '48000',
             'Agesa_EMBARGO_FUERZA_PUBLICA': '60000', 
             'Agesa_EMBARGO_FRUSTRADO': '42000', 
             'Agesa_EMBARGO_PROPIEDAD': '48000', 
             'Agesa_OP_EMBARGO': '36000', 
             'Agesa_NOT_CEDULA': '36000', 
             'Agesa_NOT_PERSONAL': '60000', 
             'Agesa_NOT_SENTENCIA': '36000',
             'Agesa_NOT_AUTO_PRUEBA': '36000', 
             'Agesa_NOT_MARTILLERO': '36000', 
             'Agesa_NOT_CBR_EMBARGO_INMUEBLE': '48000',
             'Agesa_NOT_REG_NAC_VEHICULOS_MOT': '48000',
             'Agesa_LANZANAMIENTO_FUERTO_PUBLICA': '360000', 
             'Agesa_INCAUTACION_VEHICULO': '360000', 
             'Agesa_ESCRITURA_ADJUDICACION': '96000', 
             'Agesa_DACION_PAGO': '60000',
             'Agesa_AUTORIZACION_FIRMA': '1800', 
             'Agesa_COPIAS_MANDATOS': '5040',
             'Agesa_DESARCHIVO_JUDICIAL': '6000', 
             'Agesa_OFICIOS': '1800',
             'Agesa_MANDAMIENTOS': '1800', 
             'Agesa_FOTOCOPIAS': '18000', 
             'Agesa_EXHORTOS': '6000', 
             'Agesa_NOT_AVISOS_PUBLICACION': '360000',
             'Agesa_PUBLICACION_REMATE': '360000',
             'Agesa_DOMICILIO_POSITIVO_REGION': '54000', 
             'Agesa_DOMICILIO_POSITIVIO_FUERA_REGION': '60000', 
             'Agesa_VEHICULOS_RNVM_ANNO_2000': '24000',
             'Agesa_UBICACION_INMUEBLES_REGION': '42000',
             'Agesa_UBICACION_INMUEBLES_HIPOTECADO': '13800',
             'Agesa_UBICACION_INMUEBLES_FUERA_REGION': '48000',
             'Agesa_UBICACION_INMUEBLES_FUERA_REGION_HIPOTECADO': '15840',
             'Lautaro_Rosas_BUSQUEDA_NEGATIVA': '30000', 
             'Lautaro_Rosas_BUSQUEDAS_POSITIVAS': '30000',
             'Lautaro_Rosas_NOT_DEMANDA_ART_44': '30000', 
             'Lautaro_Rosas_NOT_PERSONAL': '65000',
             'Lautaro_Rosas_REQ_PAGO_EJECUTIVO': '15000', 
             'Lautaro_Rosas_OP_EMBARGO': '15000', 
             'Lautaro_Rosas_NOT_MARTILLERO': '25000',
             'Lautaro_Rosas_NOT_PERITO': '30000', 
             'Lautaro_Rosas_NOT_CEDULA': '30000',
             'Lautaro_Rosas_NOT_CEDULA_TERCERO_AJENO_JUICIO': '25000',
             'Lautaro_Rosas_NOT_SENTENCIA': '25000',
             'Lautaro_Rosas_EMBARGO_BIENES_MUEBLES_FUERZA_PUBLICA': '65000',
             'Lautaro_Rosas_EMBARGO_BIENES_MUEBLES': '35000',
             'Lautaro_Rosas_EMBARGO_VEHICULO': '30000',
             'Lautaro_Rosas_EMBARGO_FRUSTRADO': '30000', 
             'Lautaro_Rosas_OP_RETIRO_ESPECIES': '20000',
             'Lautaro_Rosas_RETIRO_ESPECIES_FUERZA_PUBLICA': '100000',
             'Lautaro_Rosas_FLETE_RETIRO_ESPECIES': '200000', 
             'Lautaro_Rosas_INCAUTACION_VEHICULOS_NEGATIVA': '100000',
             'Lautaro_Rosas_INCAUTACION_VEHICULO_POSITIVA': '300000', 
             'Lautaro_Rosas_INSCRIPCION_EMBARGO_VEHICULO_RNVM': '30000', 
             'Lautaro_Rosas_INCAUTACION_BIENES_NEGATIVA': '60000', 
             'Lautaro_Rosas_NOT_ACREEDOR_HIP_SERVIU': '30000', 
             'Lautaro_Rosas_REQ_PAGO_JUICIO_EJECUTIVO': '20000',
             'Lautaro_Rosas_NOT_DECRETO_REMATE': '30000', 
             'Lautaro_Rosas_NOT_MEDIDA_PRECAUTORIA': '50000', 
             'Lautaro_Rosas_INSCRIPCION_EMBARGO_BIENES_CBR': '35000',
             'Lautaro_Rosas_INSCRIPCION_MEDIDA_PREJUDICIAL_PRECAUTORIA': '50000', 
             'Lautaro_Rosas_ALZAMIENTO_VEHICULOS': '40000',
             'Lautaro_Rosas_ALZAMIENTO_BIENES_INMUEBLES': '50000',
             'Santander_Natalia_EMBARGO_FRUSTRADO': '33898', 
             'Santander_Natalia_NOT_MARTILLERO': '33898',
             'Santander_Natalia_OP_RETIRO': '33989', 
             'Santander_Natalia_RET_ESPECIES': '45198',
             'Santander_Natalia_RET_ESPECIES_FLETE': '51785',
             'Santander_Natalia_RETIRO_ESPECIES_FUERZA_PUBLICA': '70586', 
             'Santander_Natalia_NOT_PRUEBA_TESTIGO': '10588',
             'Santander_Natalia_GESTORIA_DACIONES': '50000', 
             'Santander_Natalia_NOT_PERSONAL': '100000', 
             'Santander_Natalia_NOT_CEDULA_ART_44': '60000', 
             'Santander_Natalia_NOT_CEDULA': '29249',
             'Santander_Natalia_EMBARGO_PROPIEDAD': '33750', 
             'Santander_Natalia_EMBARGO_FUERZA_PUBLICA': '67997', 
             'Santander_Natalia_RETIRO_FRUSTRADO': '33989', 
             'Santander_Natalia_HONORARIOS_EXORTO': '30000',
             'Santander_Natalia_DESARCHIVO': '11299',
             'Santander_Natalia_HIPOTECA_BANCO': '30000', 
             'Santander_Natalia_BUSQUEDA_POSITIVA': '25000',
             'Santander_Natalia_BUSQUEDA_NEGATIVA': '22599', 
             'Santander_Natalia_CONSERVADOR': '56497', 
             'Santander_Natalia_GASTO_TASACION': '37000',
             'Santander_Natalia_COPIAS_AUTORIZADAS': '7910',
             'Santander_Natalia_CERTIFICADO_RVM': '1130',
             'Santander_Natalia_HONORARIOS_INCAUTADOR': '225989',
             'Santander_Natalia_INCAUTACION_RECEPTORA': '205128',
             'Santander_Natalia_BUSQUEDA_INVESTIGADOR': '28249', 
             'Santander_Natalia_CERT_HIPOTECAS_GRAVAMENES': '22599', 
             'Santander_Natalia_PUBLICACION': '385000',
             'Santander_Natalia_NOTARIA_ESCRITURA_ADJU': '395480', 
             'Santander_Natalia_EMBARGO_VEHICULO': '39548', 
             'Santander_Natalia_ALZAMIENTO_EMBARGO': '22599',
             'Santander_Natalia_PUBLICACION_PERMANENTE_DIARIO': '650000',
             'Santander_Natalia_INFO_SUMARIA_TESTIGOS': '44444', 
             'Santander_Natalia_DEFENSOR_AUSENTE': '750000', 
             'Santander_Natalia_CURADOR_HERENCIA_YACENTE': '750000',
             'Santander_Natalia_COMERCIAL': '1600', 
             'Santander_Natalia_INSCRIPCION_DOMINIO_CONSERVADOR': '250000', 
             'Santander_Natalia_PROCURADOR_NUMERO': '200000',
             'Santander_Natalia_GASTO_TASACION_PERICIAL': '1468', 
             'Santander_Natalia_REQUERIMIENTO_PAGO': '5085', 
             'Santander_Natalia_NOTARIA_DACION_PAGO': '169942',
             'Santander_Natalia_COPIA_ARCHIVO_JUDICIAL': '150000', 
             'Santander_Natalia_VIGENCIA': '15000', 
             'Santander_Natalia_COPIAS_AUTORIZADAS_EXPEDIENTE': '90395',
             'Santander_Natalia_LANZAMIENTO_FUERZA_PUBLICA': '150000', 
             'Santander_Natalia_ABSOLUCION_POSICIONES': '66667',
             'Santander_Natalia_PROPIEDAD': '106000', 
             'Santander_Natalia_PRUEBA_TESTIMONIAL': '44444', 
             'Santander_Natalia_ESCRITURA_NOTARIA_RESCILIACION': '150000',
             'Santander_Natalia_BVISTA_CAUSA': '15000', 
             'Santander_Natalia_HIPOTECA': '33333',
             'Santander_Natalia_SUBROGACION_RETENCION': '25000', 
             'Santander_Natalia_AVALUO_VEHICULO_MAXIMO_TRES_MILLONES': '287179', 
             'Santander_Natalia_AVALUO_VEHICULO_ENTRE_3_A_6_MILLONES': '338462', 
             'Santander_Natalia_AVALUO_VEHICULO_MAS_8_MILLONES': '569801', 
             'Santander_Natalia_VEHICULO_INCAUTADO_50_A_100_KMS': '68376',
             'Santander_Natalia_VEHICULO_INCAUTADO_101_A_150_KMS': '91168', 
             'Santander_Natalia_VEHICULO_INCAUTADO_201_A_250_KMS': '170940', 
             'HM_BANCO_Chile_BUSQUEDA_NEGATIVA': '15000',
             'HM_BANCO_Chile_BUSQUEDA_POSITIVA': '40000', 
             'HM_BANCO_Chile_NOT_PERSONAL_MAYOR_4_MILLONES': '80000', 
             'HM_BANCO_Chile_NOT_PERSONAL_MENOS_4_MILLONES': '60000',
             'HM_BANCO_Chile_NOT_PERSONAL_OFICINA_RECEPTOR': '30000', 
             'HM_BANCO_Chile_NOT_ART_44': '40000', 
             'HM_BANCO_Chile_OP_EMBARGO': '15000',
             'HM_BANCO_Chile_EMBARGO_FUERZA_PUBLICA': '50000', 
             'HM_BANCO_Chile_EMBARGO_VEHICULO': '30000',
             'HM_BANCO_Chile_EMBARGO_PROPIEDAD': '35000',
             'HM_BANCO_Chile_EMBARGO_TGR': '30000',
             'HM_BANCO_Chile_EMBARGO_FRUSTRADO': '25000',
             'HM_BANCO_Chile_OP_RETIRO': '25000',
             'HM_BANCO_Chile_RETIRO_FUERZA_PUBLICA': '60000',
             'HM_BANCO_Chile_RETIRO_FRUSTRADO': '30000', 
             'HM_BANCO_Chile_NOT_REGISTRO_CIVIL': '25000', 
             'HM_BANCO_ChileNOT_CBR': '30000', 
             'HM_BANCO_Chile_NOT_TGR': '25000', 
             'HM_BANCO_Chile_NOT_MARTILLERO': '25000', 
             'HM_BANCO_Chile_NOT_ART_52': '25000', 
             'HM_BANCO_Chile_NOT_VARIAS': '25000',
             'HM_BANCO_Chile_NOT_ACREEDOR_HIPOTECARIO': '25000',
             'HM_BANCO_Chile_DESCERRAJAMIENTO': '20000', 
             'HM_BANCO_Chile_FLETE_CAMION': '50000', 
             'HM_BANCO_Chile_FLETE_CAMION_FRUSTRADO': '20000', 
             'HM_BANCO_Chile_INCAUTACION_VEHICULO_LIV': '300000', 
             'HM_BANCO_Chile_INCAUTACION_VEHICULO_PESADO': '350000',
             'GMAC_hm_BUSQUEDA_NEGATIVA': '11900', 
             'GMAC_hm_BUSQUEDA_POSITIVA': '14875',
             'GMAC_hm_EMBARGO_INSCRIPCION': '38080', 
             'GMAC_hm_NOT_SENTENCIA_AUTO_PRUEBA': '29750', 
             'GMAC_hm_NOT_ATR_44': '52360', 
             'GMAC_hm_NOT_PERSONAL_REQ_PAGO': '52360', 
             'GMAC_hm_NOT_PERSONAL': '35700', 
             'GMAC_hm_NOT_CEDULA': '29750', 
             'GMAC_hm_OP_RETIRO': '26180',
             'GMAC_hm_TRAMITACION_EXHORTO_NOT': '47600',
             'GMAC_hm_ALZAMIENTO_EMBARGO_GMAC': '38080', 
             'LIDER_BCI_HM_BUSQUEDA_POSITIVA': '30000', 
             'LIDER_BCI_HM_BUSQUEDA_NEGATIVA': '14000', 
             'LIDER_BCI_HM_NOT_PERSONAL_REQUERIMIENTO': '50000', 
             'LIDER_BCI_HM_NOT_REQUERIMIENTO_JUICIO_ART_44': '45000', 
             'LIDER_BCI_HM_EMBARGO_INSC_BIEN_INMUEBLE': '55000', 
             'LIDER_BCI_HM_EMBARGO_INSC_VEHICULO': '30000',
             'LIDER_BCI_HM_DERECHO_INSC_VEHICULO': '4300', 
             'LIDER_BCI_HM_ALZAMIENTO_EMBARGO': '30000', 
             'LIDER_BCI_HM_OP_RETIRO': '15000', 
             'LIDER_BCI_HM_OP_EMBARGO_OTROS_BIENESINM': '15000', 
             'LIDER_BCI_HM_NOT_SENTENCIA_NOT_MARTILLERO_OTROS': '25000', 
             'LIDER_BCI_HM_NOT_REQUERIMIENTO_TRABA_EMB': '190000', 
             'LIDER_BCI_HM_RETIRO_VEHICULO': '170000',
             'LIDER_BCI_HM_RET_FRUSTRADO_VEHICULO': '15000',
             'LIDER_BCI_HM_RET_FUERZA_PUBLICA_OTROS_BIENES': '50000', 
             'LIDER_BCI_HM_EMB_OTROS_BIENES_FUERZA_PUB': '40000', 
             'LIDER_BCI_HM_EMB_FRUSTRADO_BIENESM': '15000', 
             'LIDER_BCI_HM_DEMANDA_800MIL': '166667', 
             'LIDER_BCI_HM_DEMANDA_1MILLON_A_3MILLONES': '277000', 
             'LIDER_BCI_HM_DEMANDA_3MILLONES_EN_ADELANTE': '322000', 
             'LIDER_BCI_HM_INV_DOMICILIO_BUSQUEDA_POSITIVA': '50000', 
             'LIDER_BCI_HM_INV_EMBARGAR_RESULTADO_POSITIVO_HEREDERO': '50000',
             'LIDER_BCI_HM_INV_CTA_CTE_SALDO_POSITIVO': '20000', 
             'LIDER_BCI_HM_AUT_REMATES_REGIONES': '60000', 
             'LIDER_BCI_HM_TRAMITACION_OFICIO': '30000', 
             'LIDER_BCI_HM_CONFF_EXHORTO': '3000', 
             'LIDER_BCI_HM_CONF_OFICIO': '3000', 
             'LIDER_BCI_HM_TRAMITACION_EXHORTO_REGIONES': '44444', 
             'LIDER_BCI_HM_TRAMITACION_MELIPILLA_BUIN_PENAFLOR': '20000', 
             'LIDER_BCI_HM_DESARCHIVO_CARTERA_REEMBOLSO': '6000', 
             'LIDER_BCI_HM_CAV_NUEVAS_ASIGNACIONES': '1000', 
             'CAJA_LOS_ANDES_BUSQUEDA_NEGATIVA': '12000', 
             'CAJA_LOS_ANDES_BUSQUEDA_POSITIVA': '30000', 
             'CAJA_LOS_ANDES_NOT_PERSONAL_REQ_EMBARGO': '70000', 
             'CAJA_LOS_ANDES_NOT_PERSONAL_REQ_OPOSICION': '70000',
             'CAJA_LOS_ANDES_EMBARGO_FUERZA_PUBLICA': '58000', 
             'CAJA_LOS_ANDES_NOT_PERSONAL_REQ_PAGO': '35000', 
             'CAJA_LOS_ANDES_NOT_ART_44': '30000',
             'CAJA_LOS_ANDES_NOTIFICACION_MARTILLERO': '20000',
             'CAJA_LOS_ANDES_NOT_CEDULA_ART_52': '16000',
             'CAJA_LOS_ANDES_NOT_AVISO_PUB_REMATE': '20000', 
             'CAJA_LOS_ANDES_OP_FISICA_EMBARGO': '15000', 
             'CAJA_LOS_ANDES_OP_RETIRO_ESPECIES': '15000', 
             'CAJA_LOS_ANDES_EMB_VEHICULO_RNVM': '30000', 
             'CAJA_LOS_ANDES_EMB_BIEN_RAIZ_CBR': '25000', 
             'CAJA_LOS_ANDES_EMB_VALORES_CTA_CTE': '28000',
             'CAJA_LOS_ANDES_EMB_FRUSTRADO': '30000', 
             'CAJA_LOS_ANDES_RETIRO_FRUSTRADO': '20000', 
             'CAJA_LOS_ANDES_RETIRO_VEHICULO': '120000', 
             'CAJA_LOS_ANDES_RETIRO_ESPECIES_FZA_PUBLICA': '40000', 
             'CAJA_LOS_ANDES_ABSOLUCION_POSICIONES': '25000', 
             'CAJA_LOS_ANDES_PRUEBA_CONFESIONAL_TESTIMONIAL': '30000', 
             'CAJA_LOS_ANDES_ALZAMIENTO_EMBARGO': '30000', 
             'TANNER_BUSQUEDA_NEGATIVA': '22759', 
             'TANNER_BUSQUEDA_NEGATIVA_AVAL': '22759', 
             'TANNER_BUSQUEDA_POSITIVA': '40759', 
             'TANNER_BUSQUEDA_POSITIVA_AVAL': '40759', 
             'TANNER_NOT_PERSONAL': '62069', 
             'TANNER_NOT_PERSONAL_AVAL': '62069',
             'TANNER_NOT_ART_44': '51724',
             'TANNER_NOT_ART_33_AVAL': '41724', 
             'TANNER_NOT_CEDULA_SENTENCIA': '25862', 
             'TANNER_NOT_CEDULA_MARTILLERO': '25862', 
             'TANNER_NOT_CEDULA_TERCEROS': '25862', 
             'TANNER_EMBARGO_INSCRIPCION_CBR': '65172', 
             'TANNER_EMBARGO_VEHICULO': '45287', 
             'TANNER_OTROS_EMBARGOS': '56897', 
             'TANNER_RETIRO_BIENES_MUEBLES_GASTOS': '56897', 
             'TANNER_OP_RET_MUEBLES': '15517', 
             'TANNER_OP_RET_VEHICULO': '30259', 
             'TANNER_INCAUTACION_VEHICULO_10MM': '230000',
             'TANNER_INCAUTACION_VEHICULO': '226436',
             'TANNER_EMBARGO_FRUSTRADO': '15517',
             'TANNER_RETIRO_FRUSTRADO': '34138', 
             'TANNER_DISTANCIA_COMUNA_PTEALTO_PADREHURT': '11322', 
             'TANNER_DISTANCIA_SANMIGUEL': '9057', 
             'TANNER_ALZAMIENTO_EMBARGO': '31034',
             'LOPEZ_SA_BUSQUEDA_NEGATIVA': '12000',
             'LOPEZ_SA_BUSQUEDA_POSITIVA': '15000', 
             'LOPEZ_SA_NOT_REQUERIMIENTO_OP': '34000',
             'LOPEZ_SA_NOT_ART_44': '22000', 
             'LOPEZ_SA_EMBARGO_POSITIVO_FZA_PUBLICA': '28000', 
             'LOPEZ_SA_EMBARGO_FRUSTRADO': '24000', 
             'LOPEZ_SA_NOT_MARTILLERO': '22000', 
             'LOPEZ_SA_OP_RETIRO_ESPECIES': '10000', 
             'LOPEZ_SA_RET_POSITIVO': '30000',
             'LOPEZ_SA_RET_NEGATIVO': '20000', 
             'LOPEZ_SA_NOT_ARRESTO': '15000', 
             'LOPEZ_SA_NOT_ART_52': '15000', 
             'ELVEN_ASESORIAS_BUSQUEDA_POSITIVA': '10000', 
             'ELVEN_ASESORIAS_BUSQUEDA_NEGATIVA': '8000', 
             'ELVEN_ASESORIAS_NOT_CEDULA_OP_EMBARGO': '16000', 
             'ELVEN_ASESORIAS_NOT_PERS_OP_EMBARGO': '26000',
             'ELVEN_ASESORIAS_EMBARGO_POSITIVO': '35000', 
             'ELVEN_ASESORIAS_EMBARGO_NEGATIVO': '15000', 
             'ELVEN_ASESORIAS_EMBARGO_POSITIVO_CTA_CTE': '26000', 
             'ELVEN_ASESORIAS_EMBARGO_NEGATIVO_CTA_CTE': '15000', 
             'ELVEN_ASESORIAS_NOT_MARTILLERO': '15000', 
             'ELVEN_ASESORIAS_OP_RETIRO': '15000', 
             'ELVEN_ASESORIAS_NOT_ART_52': '8000', 
             'ELVEN_ASESORIAS_RET_ESPECIES_FRUSTRADO': '15000', 
             'ELVEN_ASESORIAS_RET_ESPECIES_POSITIVO': '35000', 
             'SOCOFIN_BUSQUEDA_NEGATIVA': '15000', 
             'SOCOFIN_BUSQUEDA_POSITIVA': '40000', 
             'SOCOFIN_NOT_PERSONAL_MAYOR_4MILLONES': '60000', 
             'SOCOFIN_NOT_PERSONAL_GARANTIA': '60000', 
             'SOCOFIN_NOT_PERSONAL_MENOR_4MILLONES': '50000',
             'SOCOFIN_NOT_PERSONAL_RECEPTOR': '25000',
             'SOCOFIN_NOT_ART_44_CPC': '50000', 
             'SOCOFIN_OP_EMBARGO': '5000', 
             'SOCOFIN_EMBARGO_FUERZA_PUBLICA': '45000', 
             'SOCOFIN_EMBARGO_VEHICULO': '20000', 
             'SOCOFIN_EMBARGO_PROPIEDAD': '50000', 
             'SOCOFIN_EMBARGO_TESORERIA': '20000', 
             'SOCOFIN_EMBARGO_RNVM': '18000', 
             'SOCOFIN_NOT_CBR': '18000', 
             'SOCOFIN_NOT_TESORERIA': '18000', 
             'SOCOFIN_EMBARGO_FRUSTRADO': '15000', 
             'SOCOFIN_OP_RETIRO': '15000', 
             'SOCOFIN_RET_FUERZA_PUBLICA': '50000', 
             'SOCOFIN_RET_FRUSTRADO': '20000', 
             'SOCOFIN_NOT_MARTILLERO': '18000', 
             'SOCOFIN_NOT_ART_52': '18000', 
             'SOCOFIN_NOT_VARIAS': '18000', 
             'SOCOFIN_NOT_ACREEDOR_HIPOTECARIO': '18000', 
             'SOCOFIN_DESCERRAJAMIENTO': '10000', 
             'SOCOFIN_FLETE_CAMION': '30000', 
             'SOCOFIN_INCAUTACION_VEHICULO_LIVIANO': '250000', 
             'SOCOFIN_INCAUTACION_VEHICULO_PESADO': '350000',
             'ORPRO_BUSQUEDA_NEGATIVA': '10500', 
             'ORPRO_BUSQUEDA_POSITIVA': '9000',
             'ORPRO_NOT_PERSONAL_OP': '25000', 
             'ORPRO_NOT_PERSONAL_EMBARGO': '32000', 
             'ORPRO_NOT_ART_44_OP': '30000', 
             'ORPRO_EMBARGO_FUERZA_PUBLICA': '20000',
             'ORPRO_EMBARGO_FRUSTRADO_FUERZA_PUB': '15000', 
             'ORPRO_NOT_MARTILLERO': '15000',
             'ORPRO_OP_RETIRO_ESPECIES': '6000',
             'ORPRO_RET_ESPECIES': '30000',
             'ORPRO_RET_FRUSTRADO': '15000',
             'ORPRO_NOT_ARRESTO': '15000',
             'ORPRO_NOT_ART_52': '16000',
             'ORPRO_NOT_CEDULA': '16000',
             'ORPRO_NOT_EMBARGO_BIEN_RAIZ': '20000', 
             'ORPRO_NOT_REGISTRO_CIVIL': '20000'}
        
        for key in sorted(self.aranceles.keys()):
            self.combo_letters.addItem(key)

    def on_combo_letters_changed(self, index):
        selected_key = self.combo_letters.currentText()
        arancel_value = self.aranceles[selected_key]
        self.combo_numbers.clear()
        self.combo_numbers.addItems([arancel_value])
        self.selected_item = selected_key
        print(arancel_value)

    def update_number_combo_box(self, letter):
        self.combo_numbers.clear()
        arancel_value = self.aranceles[letter]
        self.combo_numbers.addItem(arancel_value)
        
    def actualizar_tabla(self, arancel_value):
        selected_key = self.combo_letters.currentText()
        arancel_value = self.aranceles[selected_key]

        if self.selected_item is None:
            QMessageBox.critical(self, "Error", "Debe seleccionar un arancel antes de actualizar la tabla.")
            return

        try:
            conn = mysql.connector.connect(host='vps-3697915-x.dattaweb.com', user='daniel', password='LOLxdsas--', database='micau5a')
            cursor = conn.cursor()

            query = """UPDATE notificacion SET arancel = %s WHERE numjui = %s"""
            cursor.execute(query, (arancel_value, self.numjui))
          
            conn.commit()
            conn.close()

            QMessageBox.information(self, "Éxito", "La tabla ha sido actualizada correctamente.")

        except Exception as e:
            logging.error(f"Error al actualizar la tabla: {str(e)}")
            QMessageBox.critical(self, "Error", "Ha ocurrido un error al actualizar la tabla. Consulte al administrador.")
            return


if __name__ == "__main__":
    app = QApplication(sys.argv)
    dialog = ActualizarArancelDialog(fechaNotificacion='', numjui='', nombTribunal='', demandante='', demandado='', repre='', mandante='', domicilio='', comuna='', encargo='', soli='', arancel='')
    dialog.show()
    sys.exit(app.exec())
