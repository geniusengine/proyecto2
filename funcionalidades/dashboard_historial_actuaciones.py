import os
import sys
import time
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QTableWidget, \
    QTableWidgetItem, QHeaderView, QCheckBox, QHBoxLayout , QMessageBox, QLabel,QComboBox, QToolButton, QMenu
from PyQt6.QtGui import QColor, QIcon
from PyQt6.QtCore import QDateTime, QTimer, Qt, pyqtSignal
import pymssql
from datetime import datetime
import logging
from docx import Document
from docx2pdf import convert
from tkinter import filedialog
import tkinter as tk


# Configurar el sistema de registro
logging.basicConfig(filename='registro.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class DashboardHistorialActuaciones(QMainWindow):
    def __init__(self):


        super().__init__()
        self.db_connection = None
        self.datos = []
        self.initUI()
        print("Dashboard Actuaciones")
    
    def initUI(self):
        self.setWindowTitle('Historial Actuaciones')
        self.setWindowIcon(QIcon("static/icono-ventana.png"))
        self.setGeometry(100, 100, 1280, 720)

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)
        self.layout_vertical = QVBoxLayout()  # Crea un layout vertical
        self.layout_horizontal = QHBoxLayout()  # Crea un layout horizontal
   
        self.layout_horizontal.addLayout(self.layout_vertical)# Agrega el layout vertical al layout horizontal

        # Crea una tabla y un botón de guardar
        self.table = QTableWidget()
        # Establecer el color de las líneas de las celdas
        self.table.setStyleSheet(
        "QTableView { gridline-color: white; }"
        "QTableCornerButton::section { background-color: #d3d3d3; border: 1px solid black; }"
        "QHeaderView::section { background-color: #d3d3d3; border: 1px solid black; }"
        )
        self.layout_vertical.addWidget(self.table)# Agrega la tabla al layout vertical
    
        # Conectar la señal de clic en el encabezado de la columna para ordenar
        self.table.horizontalHeader().sectionClicked.connect(self.ordenar_tabla)

        # Configuraciones finales del diseño
        self.central_widget.setLayout(self.layout_horizontal)

        # Llama automáticamente a acceder_base_de_datos y mostrar_clicked al iniciar la aplicación
        self.establecer_conexion_base_de_datos()
        self.obtener_datos()
        self.mostrar_tabla()

        self.setGeometry(100, 100, 400, 300)


    def combo_box_changed(self, row, col, index):
        # Aquí deberías escribir el código que se ejecutará cuando cambie el índice del combo box
        pass

    # crea cada boton que se necesite
    def crear_boton(self, texto, funcion):
        boton = QPushButton(texto, self)
        boton.clicked.connect(funcion)
        return boton
    # crea un boton con un icono
    def crear_boton_con_icono(self, icono_path, funcion):
        boton = QPushButton(self)
        icono = QIcon(icono_path)
        boton.setIcon(icono)
        boton.clicked.connect(funcion)
        return boton
    
    def update_dashboard(self):
        # Esta función se llamará cuando se guarden los datos
        self.label.setText("¡Panel Actualizado!")
        
        
    # establece la conexion con la base de datos
    def establecer_conexion_base_de_datos(self):
        self.db_connection = pymssql.connect(
            server='vps-3697915-x.dattaweb.com',
            user='daniel',
            password='LOLxdsas--',
            database='micau5a'
        )
    # cierra la conexion con la base de datos
    def cerrar_conexion_base_de_datos(self):
        if self.db_connection:
            self.db_connection.close()


# limpia la tabla
    def limpiar_tabla(self):
        self.table.clearContents()
        self.table.setRowCount(0)
# obtiene la fecha actual
    def obtener_fecha_actual(self):
        # Obtener la fecha y hora actual
        fecha_actual = QDateTime.currentDateTime()
        # Formatear la fecha y hora
        formato_fecha = fecha_actual.toString('yyyy-MM-dd HH:mm:ss')
        return formato_fecha
# ajusta el tamaño de la tabla ajustándose al contenido
    def ajustar_tamanio(self):
        self.table.resizeColumnsToContents()
        total_width = sum(self.table.columnWidth(col) for col in range(self.table.columnCount()))
        min_width = max(self.width(), total_width)
        
        # Establecer un ancho máximo para la ventana
        max_width = 1000  # Puedes ajustar este valor según tus necesidades
        min_width = min(min_width, max_width)
        
        self.setMinimumWidth(min_width - 260)
        self.setMaximumWidth(max_width)  # Establecer un ancho máximo para la ventana
        self.adjustSize()
    # ...
    def establecer_conexion_base_de_datos(self):
        try:
            self.db_connection = pymssql.connect(
                server='vps-3697915-x.dattaweb.com',
                user='daniel',
                password='LOLxdsas--',
                database='micau5a'
            )
        except Exception as e:
            print(f"Error al establecer la conexión: {e}")

    def cerrar_conexion_base_de_datos(self):
        try:
            if self.db_connection:
                self.db_connection.close()
        except Exception as e:
            print(f"Error al cerrar la conexión: {e}")

    def obtener_datos(self):
        
        try:
            self.establecer_conexion_base_de_datos()
            with self.db_connection.cursor() as cursor:
                query = "SELECT fechaNotificacion, numjui, nombTribunal, nombdemandante, apellidemandante, demandado, repre, mandante, domicilio, comuna, encargo, soli, arancel, estadoNoti, estadoCausa FROM AUD_notificacion"
                
        
                
                cursor.execute(query)
                resultados = cursor.fetchall()
                
                
            self.causas=[]
            for fila in resultados:
                causa = {'fechaNotificacion':fila[0],'numjui':fila[1],'nombtribunal':fila[2],'nomdemandante':fila[3],'apellidemandante':fila[4],'demandado':fila[5],'repre':fila[6],'mandante':fila[7],'domicilio':fila[8],'comuna':fila[9],'encargo':fila[10],'soli':fila[11],'arancel':fila[12], 'actuacion':'actuacion'}
                    
                
                self.causas.append(causa)
        except Exception as e:
            print(f"Error al acceder a la base de datos: {e}")
        finally:
            self.cerrar_conexion_base_de_datos()


        
# muestra los datos en la tabla
    def mostrar_tabla(self):
        self.table.setColumnCount(14)
        self.table.setHorizontalHeaderLabels(['fechaNotificacion', 'Rol', 'Tribunal', 'Nombre demandante', 'Apellido demandante', 'Nombre demandado', 'Representante', 'Quien Encarga', 'Domicilio', 'Comuna', 'Encargo', 'Resultado', 'Arancel', 'Actuación'])
        for row_index, causa in enumerate(self.causas):
            
            self.table.insertRow(row_index)
            for col_index, (key, value) in enumerate(causa.items()):
                        if key == "actuacion":
                        # Crear un objeto QComboBox para las celdas de actuaciones
                            combo_box = QComboBox()
                            opciones_actuaciones = ["Elija actuación", "Búsqueda Negativa", "Búsqueda Positiva", "Not. por cédula", "Not. Art. 44", "Req. de pago en Oficina", "Op. al Embargo", "Not. Personal", "Not. Personal/Req. de Pago", "Not. art. 52", "Embargo con Fuerza Pública", "Embargo Frustrado", "Embargo Banco", "Embargo Vehículo", "Retiro de Vehículo", "Retiro Frustrado", "Retiro de Especies ", "OtrO"]
                            combo_box.addItems(opciones_actuaciones)
                            combo_box.setCurrentText(value)
                            self.table.setCellWidget(row_index, col_index, combo_box)
                            combo_box.currentIndexChanged.connect(lambda index, row=row_index, col=col_index: self.combo_box_changed(row, col, index))
                        else:
                        # Crea un objeto QTableWidgetItem para las otras columnas
                            item = QTableWidgetItem(str(value))
                        # establece el color de la celda
                            item.setBackground(QColor(52, 152, 219))
                            self.table.setItem(row_index, col_index, item)
                    
        self.ajustar_tamanio()
# Función para ordenar la tabla según la columna clicada
    def ordenar_tabla(self, logicalIndex):
        self.table.sortItems(logicalIndex, Qt.SortOrder.AscendingOrder if self.table.horizontalHeader().sortIndicatorOrder() == Qt.SortOrder.DescendingOrder else Qt.SortOrder.DescendingOrder)
        
    def combo_box_changed(self, row, col, index):
        # Obtén el valor actual del combo box
        combo_box = self.table.cellWidget(row, col)
        selected_value = combo_box.currentText()

        # Verifica si el valor seleccionado es "Búsqueda Negativa"
        if selected_value == "Búsqueda Negativa":
            # Llama al método negativaP para realizar el estampado
            self.negativaP(row)

        elif selected_value == "Búsqueda Positiva":
            #Llama al método negativaP para realizar el estampado
            self.positivaP(row)

        elif selected_value == "Not. por cédula":
            #Llama al método negativaP para realizar el estampado
            self.notificacionPorCedula(row)

        elif selected_value == "Not. Art. 44":
            #Llama al método negativaP para realizar el estampado
            self.notificacion44(row)
        
        elif selected_value == "Req. de pago en Oficina":
            #Llama al método negativaP para realizar el estampado
            self.actaRequerimientoPago(row)
        
        elif selected_value == "Op. al Embargo":
            #Llama al método negativaP para realizar el estampado
            self.actaOposicionEmbargo(row)
        
        elif selected_value == "Not. Personal":
            #Llama al método negativaP para realizar el estampado
            self.notificacionpecausaperuanoqliao(row)
        
        elif selected_value == "Not. Personal/Req. de Pago":
            #Llama al método negativaP para realizar el estampado
            self.actaRequerimientoPago(row)

        elif selected_value == "Not. art. 52":
            #Llama al método negativaP para realizar el estampado
            self.busquedaN(row)
        
        elif selected_value == "Embargo con Fuerza Pública":
            #Llama al método negativaP para realizar el estampado
            self.fuerzapu(row)

        elif selected_value == "Embargo Frustrado":
            #Llama al método negativaP para realizar el estampado
            self.EMBARGOFRUSTRADO(row)

        elif selected_value == "Embargo Banco":
            #Llama al método negativaP para realizar el estampado
            self.bban(row)

        elif selected_value == "Embargo Vehículo":
            #Llama al método negativaP para realizar el estampado
            self.embargoauto(row)

        


    def negativaP(self, row):
        # Obtén los datos de la fila seleccionada
        fechaNotificacion = self.table.item(row, 0).text()
        numjui = self.table.item(row, 1).text()  
        nombTribunal = self.table.item(row, 2).text()  
        nombdemandante = self.table.item(row, 3).text()
        apellidemandante = self.table.item(row, 4).text()  
        demandado = self.table.item(row, 5).text()  
        repre = self.table.item(row, 6).text()  
        mandante = self.table.item(row, 7).text()  
        domicilio = self.table.item(row, 8).text()  
        comuna = self.table.item(row, 9).text()  
        encargo = self.table.item(row, 10).text() 
        soli = self.table.item(row, 11).text() 
        arancel = self.table.item(row, 12).text()

        
        # variables de tiempo lel
        now = datetime.now()
        años = now.strftime("%d/%m/%y")
        horas = now.strftime("%H:%M")

        # Crea un nuevo documento de Word
        doc = Document()

        # Agrega el encabezado con los marcadores de posición
        encabezado = f"{nombTribunal}\n{numjui}  :  {encargo}\n {nombdemandante} {apellidemandante} CON {demandado}"
        doc.add_paragraph(encabezado)

        # Agrega la sección de búsqueda negativa con los datos proporcionados
        busqueda_negativaP = f"BÚSQUEDA NEGATIVA: Certifico haber buscado al(la) demandado(a) {demandado} con domicilio en {domicilio} {comuna}, especialmente el día {años}, siendo las {horas} horas, a fin de notificarle la demanda íntegra y su respectivo proveído. Diligencia que no se llevó a efecto por cuanto el(la) demandado(a) no fue habido(a), {soli}. DOY FE."
        doc.add_paragraph(busqueda_negativaP)

        # Agrega la firma al final del documento
        doc.add_paragraph(f"Drs. {arancel}.-")

        # Abre un cuadro de diálogo para seleccionar el directorio donde se guardará el documento
        root = tk.Tk()
        root.withdraw()  # Oculta la ventana de Tkinter
        save_path = filedialog.askdirectory()  # Abre el cuadro de diálogo

         # Guarda el documento en el directorio seleccionado
        doc.save(os.path.join(save_path, f'{self.numjui} {self.nombTribunal} {self.fechaNotificacion}.docx'))

        logging.info(f'A estamapado {numjui}-{encargo}')  
    
    def positivaP(self, row):
        # Obtén los datos de la fila seleccionada
        fechaNotificacion = self.table.item(row, 0).text()
        numjui = self.table.item(row, 1).text()  
        nombTribunal = self.table.item(row, 2).text()  
        nombdemandante = self.table.item(row, 3).text()
        apellidemandante = self.table.item(row, 4).text()  
        demandado = self.table.item(row, 5).text()  
        repre = self.table.item(row, 6).text()  
        mandante = self.table.item(row, 7).text()  
        domicilio = self.table.item(row, 8).text()  
        comuna = self.table.item(row, 9).text()  
        encargo = self.table.item(row, 10).text() 
        soli = self.table.item(row, 11).text() 
        arancel = self.table.item(row, 12).text()

        now = datetime.now()
        años = now.strftime("%d/%m/%y")
        horas = now.strftime("%H:%M")
        
        # Crea un nuevo documento de Word
        doc = Document()

        # Agrega el encabezado con los marcadores de posición
        encabezado = f"{nombTribunal}\n{numjui}  :  {encargo}\n {nombdemandante} {apellidemandante} CON {demandado}"
        doc.add_paragraph(encabezado)

        # Agrega la sección de búsqueda negativa con los datos proporcionados
        busqueda_positiva = f"BÚSQUEDA POSITIVA:a {años}, siendo las {horas} horas, en su domicilio ubicado en {domicilio} {comuna}, busqué a {nombdemandante} {apellidemandante}, a fin de notificarle la demanda íntegra y su respectivo proveído, diligencia que no se llevó a efecto por no ser habido en dicho domicilio, en ese momento. Por los dichos de {soli}.DOY FE."
        doc.add_paragraph(busqueda_positiva)

        # Agrega la firma al final del documento
        doc.add_paragraph(f"Drs. {arancel}.-")

        # Abre un cuadro de diálogo para seleccionar el directorio donde se guardará el documento
        root = tk.Tk()
        root.withdraw()  # Oculta la ventana de Tkinter
        save_path = filedialog.askdirectory()  # Abre el cuadro de diálogo

         # Guarda el documento en el directorio seleccionado
        doc.save(os.path.join(save_path, f'{self.numjui} {self.nombTribunal} {self.fechaNotificacion}.docx'))

        logging.info(f'A estamapado {numjui}-{encargo}')

    def notificacionPorCedula(self, row):

        fechaNotificacion = self.table.item(row, 0).text()
        numjui = self.table.item(row, 1).text()  
        nombTribunal = self.table.item(row, 2).text()  
        nombdemandante = self.table.item(row, 3).text()
        apellidemandante = self.table.item(row, 4).text()  
        demandado = self.table.item(row, 5).text()  
        repre = self.table.item(row, 6).text()  
        mandante = self.table.item(row, 7).text()  
        domicilio = self.table.item(row, 8).text()  
        comuna = self.table.item(row, 9).text()  
        encargo = self.table.item(row, 10).text() 
        soli = self.table.item(row, 11).text() 
        arancel = self.table.item(row, 12).text()

        # Variables de tiempo
        now = datetime.now()
        fecha_actual = now.strftime("%d/%m/%Y")
        hora_actual = now.strftime("%H:%M")

        # Crea un nuevo documento de Word
        doc = Document()

        # Agrega el encabezado con los marcadores de posición
        encabezado = f"{nombTribunal}\n{numjui} : {encargo} \n {nombdemandante} {apellidemandante} CON {demandado}"
        doc.add_paragraph(encabezado)

        # Agrega la sección de notificación por cédula
        notificacion_cedula = f"NOTIFICACIÓN POR CÉDULA: a {fecha_actual}, siendo las {hora_actual} horas, en su domicilio ubicado en {domicilio}, {comuna}, notifiqué por cédula a {demandado} representado por {repre}, a fin de notificarle la resolución de fecha **, la resolución de fecha **. La cédula conteniendo copia íntegra de lo notificado fue **. DOY FE.\n"
        notificacion_cedula += f"Drs. {arancel}.-"
        doc.add_paragraph(notificacion_cedula)

        # Abre un cuadro de diálogo para seleccionar el directorio donde se guardará el documento
        root = tk.Tk()
        root.withdraw()  # Oculta la ventana de Tkinter
        save_path = filedialog.askdirectory()  # Abre el cuadro de diálogo

        # Guarda el documento en el directorio seleccionado
        doc.save(os.path.join(save_path, f'{self.numjui} {self.nombTribunal} {self.fechaNotificacion}.docx'))

        logging.info(f'A estampado {numjui}-{encargo}')

    def notificacion44(self, row):
        
        fechaNotificacion = self.table.item(row, 0).text()
        numjui = self.table.item(row, 1).text()  
        nombTribunal = self.table.item(row, 2).text()  
        nombdemandante = self.table.item(row, 3).text()
        apellidemandante = self.table.item(row, 4).text()  
        demandado = self.table.item(row, 5).text()  
        repre = self.table.item(row, 6).text()  
        mandante = self.table.item(row, 7).text()  
        domicilio = self.table.item(row, 8).text()  
        comuna = self.table.item(row, 9).text()  
        encargo = self.table.item(row, 10).text() 
        soli = self.table.item(row, 11).text() 
        arancel = self.table.item(row, 12).text()

        # Variables de tiempo
        now = datetime.now()
        fecha_actual = now.strftime("%d/%m/%Y")
        hora_actual = now.strftime("%H:%M")

        # Crea un nuevo documento de Word
        doc = Document()

        # Agrega el encabezado con los marcadores de posición
        encabezado = f"{nombTribunal}\n{numjui} : {encargo} \n {nombdemandante} {apellidemandante} CON {demandado}"
        doc.add_paragraph(encabezado)

        # Agrega la sección de notificación personal subsidiaria
        notificacion_subsidiaria = f"NOTIFICACIÓN PERSONAL SUBSIDIARIA: A {fecha_actual}, siendo las {hora_actual} horas, en su domicilio ubicado en {domicilio}, {comuna}, notifiqué a {demandado}, representado por {repre}, se constató que es su domicilio y que se encuentra en el lugar del juicio por **, en conformidad al artículo 44 inciso segundo del Código de Procedimiento Civil modificado por el artículo 3, N°3 letra A y B de la ley N°21.394, la demanda íntegra, su respectivo proveído. Copia íntegra de lo notificado fue **. Doy fe.\n"
        notificacion_subsidiaria += f"Búsqueda: **.-\nDrs: {arancel}.-"
        doc.add_paragraph(notificacion_subsidiaria)

        # Agrega la sección de cédula de espera
        cedula_espera = f"CÉDULA DE ESPERA: A **, siendo las ** horas, en su domicilio ubicado en {domicilio}, {comuna}, busqué a {demandado}, representado por {repre}, y notifiqué el mandamiento de fs.01, por cédula. Dejé citado (a) al demandado (a) a fin de que concurra a mi oficio ubicado en calle Av. Del Mar, N° 5.700, of. N° 47 La Serena., el día **, a las ** horas, a fin de requerirlo (a) personalmente de pago, bajo apercibimiento de que si no comparece, será declarado (a) requerido (a) de pago en rebeldía y se le practicará sin más trámite el embargo.\n"
        cedula_espera += "Para constancia levanté la presente acta. Doy fe.-"
        doc.add_paragraph(cedula_espera)

        # Abre un cuadro de diálogo para seleccionar el directorio donde se guardará el documento
        root = tk.Tk()
        root.withdraw()  # Oculta la ventana de Tkinter
        save_path = filedialog.askdirectory()  # Abre el cuadro de diálogo

        # Guarda el documento en el directorio seleccionado
        doc.save(os.path.join(save_path, f'{self.numjui} {self.nombTribunal} {self.fechaNotificacion}.docx'))

        logging.info(f'A estampado {numjui}-{encargo}')

    def actaRequerimientoPago(self,row):

        fechaNotificacion = self.table.item(row, 0).text()
        numjui = self.table.item(row, 1).text()  
        nombTribunal = self.table.item(row, 2).text()  
        nombdemandante = self.table.item(row, 3).text()
        apellidemandante = self.table.item(row, 4).text()  
        demandado = self.table.item(row, 5).text()  
        repre = self.table.item(row, 6).text()  
        mandante = self.table.item(row, 7).text()  
        domicilio = self.table.item(row, 8).text()  
        comuna = self.table.item(row, 9).text()  
        encargo = self.table.item(row, 10).text() 
        soli = self.table.item(row, 11).text() 
        arancel = self.table.item(row, 12).text()

        # Variables de tiempo
        now = datetime.now()
        fecha_actual = now.strftime("%d/%m/%Y")
        hora_actual = now.strftime("%H:%M")

        # Crea un nuevo documento de Word
        doc = Document()

        # Agrega el encabezado con los marcadores de posición
        encabezado = f"{nombTribunal}\n{numjui}: {encargo}\n{nombdemandante} {apellidemandante} CON {demandado}"
        doc.add_paragraph(encabezado)

        # Agrega la sección de acta de requerimiento de pago en rebeldía
        acta_requerimiento_pago = f"ACTA DE REQUERIMIENTO DE PAGO EN REBELDÍA: En La Serena, a {fecha_actual}, siendo las {hora_actual} horas, en mi oficio ubicado en Av. Del Mar, N° 5.700, of. N° 47 La Serena, no habiendo comparecido el (la) demandado (a), don (ña) {demandado}, representado por {repre}, lo (la) doy por requerido(a) de pago en rebeldía por la suma de pesos, más reajustes, intereses, recargos.\n\n"
        acta_requerimiento_pago += "NO SE EFECTUÓ EL PAGO.\n"
        acta_requerimiento_pago += "Tiene el (la) ejecutado (da) el plazo legal de 8 días hábiles para oponer excepciones a la ejecución.\n"
        acta_requerimiento_pago += "Para constancia levanté la presente acta. Doy fe.\n\n"
        acta_requerimiento_pago += f"Drs. + gastos. $ {arancel}.-"
        doc.add_paragraph(acta_requerimiento_pago)

        # Abre un cuadro de diálogo para seleccionar el directorio donde se guardará el documento
        root = tk.Tk()
        root.withdraw()  # Oculta la ventana de Tkinter
        save_path = filedialog.askdirectory()  # Abre el cuadro de diálogo

        # Guarda el documento en el directorio seleccionado
        doc.save(os.path.join(save_path, f'{self.numjui} {self.nombTribunal} {self.fechaNotificacion}.docx'))

        logging.info(f'A estampado {numjui}-{encargo}')

    def actaOposicionEmbargo(self,row):

        fechaNotificacion = self.table.item(row, 0).text()
        numjui = self.table.item(row, 1).text()  
        nombTribunal = self.table.item(row, 2).text()  
        nombdemandante = self.table.item(row, 3).text()
        apellidemandante = self.table.item(row, 4).text()  
        demandado = self.table.item(row, 5).text()  
        repre = self.table.item(row, 6).text()  
        mandante = self.table.item(row, 7).text()  
        domicilio = self.table.item(row, 8).text()  
        comuna = self.table.item(row, 9).text()  
        encargo = self.table.item(row, 10).text() 
        soli = self.table.item(row, 11).text() 
        arancel = self.table.item(row, 12).text()

        now = datetime.now()
        fecha_actual = now.strftime("%d/%m/%Y")
        hora_actual = now.strftime("%H:%M")

        # Crea un nuevo documento de Word
        doc = Document()

        # Agrega el encabezado con los marcadores de posición
        encabezado = f"{nombTribunal}\n{numjui} : {encargo} \n {nombdemandante} {apellidemandante} CON {demandado}"
        doc.add_paragraph(encabezado)

        # Agrega la sección de acta de oposición a embargo
        acta_oposicion_embargo = f"ACTA DE OPOSICION A EMBARGO: a {fecha_actual}, siendo las {hora_actual} horas, concurrí al domicilio ubicado en {domicilio}, {comuna}, notifiqué a {demandado}, representado por {repre}, con el objeto de proceder a trabar embargo sobre bienes de su propiedad, diligencia que no pude efectuar, por OPOSICIÓN AL EMBARGO, por **. DOY FE.\n"
        acta_oposicion_embargo += f"Drs. {arancel}.-"
        doc.add_paragraph(acta_oposicion_embargo)

        # Abre un cuadro de diálogo para seleccionar el directorio donde se guardará el documento
        root = tk.Tk()
        root.withdraw()  # Oculta la ventana de Tkinter
        save_path = filedialog.askdirectory()  # Abre el cuadro de diálogo

        # Guarda el documento en el directorio seleccionado
        doc.save(os.path.join(save_path, f'{self.numjui} {self.nombTribunal} {self.fechaNotificacion}.docx'))

        logging.info(f'A estampado {numjui}-{encargo}')

    def notificacionpecausaperuanoqliao(self, row):
        
        fechaNotificacion = self.table.item(row, 0).text()
        numjui = self.table.item(row, 1).text()  
        nombTribunal = self.table.item(row, 2).text()  
        nombdemandante = self.table.item(row, 3).text()
        apellidemandante = self.table.item(row, 4).text()  
        demandado = self.table.item(row, 5).text()  
        repre = self.table.item(row, 6).text()  
        mandante = self.table.item(row, 7).text()  
        domicilio = self.table.item(row, 8).text()  
        comuna = self.table.item(row, 9).text()  
        encargo = self.table.item(row, 10).text() 
        soli = self.table.item(row, 11).text() 
        arancel = self.table.item(row, 12).text()    
        
        # variables de tiempo lel
        now = datetime.now()
        fecha_actual = now.strftime("%d/%m/%Y")
        hora_actual = now.strftime("%H:%M")

        # Crea un nuevo documento de Word
        doc = Document()

        encabezado = f"{nombTribunal}\n{numjui}  :  {encargo}\n {nombdemandante} {apellidemandante} CON {demandado}"
        doc.add_paragraph(encabezado)

        notificacionPeruano = f'NOTIFICACIÓN PERSONAL:En la Comuna de {comuna} a {fecha_actual}, siendo las {hora_actual} horas, en su domicilio ubicado {domicilio}, {comuna}, notifiqué personalmente a {demandado}, representado por {repre},  la demanda  y su respectivo proveído. Le hice entrega de copia íntegra de lo notificado y no firmó. La identidad del notificado/a  se estableció por los datos aportados por el mismo. DOY FE.'
        doc.add_paragraph(notificacionPeruano)

        doc.add_paragraph(f"Drs. {arancel}.-")

        # Abre un cuadro de diálogo para seleccionar el directorio donde se guardará el documento
        root = tk.Tk()
        root.withdraw()  # Oculta la ventana de Tkinter
        save_path = filedialog.askdirectory()  # Abre el cuadro de diálogo

         # Guarda el documento en el directorio seleccionado
        doc.save(os.path.join(save_path, f'{self.numjui} {self.nombTribunal} {self.fechaNotificacion}.docx'))

        logging.info(f'A estamapado {numjui}-{encargo}')


    def actaRequerimientoPago(self,row):

        fechaNotificacion = self.table.item(row, 0).text()
        numjui = self.table.item(row, 1).text()  
        nombTribunal = self.table.item(row, 2).text()  
        nombdemandante = self.table.item(row, 3).text()
        apellidemandante = self.table.item(row, 4).text()  
        demandado = self.table.item(row, 5).text()  
        repre = self.table.item(row, 6).text()  
        mandante = self.table.item(row, 7).text()  
        domicilio = self.table.item(row, 8).text()  
        comuna = self.table.item(row, 9).text()  
        encargo = self.table.item(row, 10).text() 
        soli = self.table.item(row, 11).text() 
        arancel = self.table.item(row, 12).text() 

       # Variables de tiempo
        now = datetime.now()
        fecha_actual = now.strftime("%d/%m/%Y")
        hora_actual = now.strftime("%H:%M")

        # Crea un nuevo documento de Word
        doc = Document()

        # Agrega el encabezado con los marcadores de posición
        encabezado = f"{nombTribunal}\n{numjui} : {encargo} \n {nombdemandante} {apellidemandante} CON {demandado}"
        doc.add_paragraph(encabezado)

        # Agrega la sección de requerimiento de pago y oposición a embargo
        requerimiento_oposicion_texto = f"REQUERIMIENTO DE PAGO PERSONAL Y OPOSICIÓN A EMBARGO: A {fecha_actual}, siendo las {hora_actual} horas, en su domicilio ubicado en {domicilio}, {comuna}, notifiqué el mandamiento de **, y requerí personalmente de pago a {demandado}, representado por {repre}, a fin de que en el acto pague a {nombdemandante} {apellidemandante}, o a quien sus derechos represente, la suma de ** (** pesos), más reajustes, intereses y recargos.\n"
        requerimiento_oposicion_texto += f"NO SE EFECTUÓ EL PAGO. Le hice presente la orden de embargo sobre bienes de su propiedad, en cantidad suficiente que permita cubrir el valor total de lo adeudado, más los gastos de la ejecución. También le notifiqué su designación como depositario provisional de los bienes que se le embarguen, cargo que aceptó, jurando su fiel desempeño y además le hice presente el plazo legal que tiene para deducir excepciones a la ejecución.\n"
        requerimiento_oposicion_texto += f"Acto seguido intenté trabar embargo sobre bienes de su propiedad, diligencia que no se llevó a efecto por OPOSICIÓN DEL PROPIO DEMANDADO.\n"
        requerimiento_oposicion_texto += f"Para constancia levanté la presente acta que la ejecutada no firmó, entregándole en el acto copia del mandamiento. Doy Fe."
        doc.add_paragraph(requerimiento_oposicion_texto)

        # Abre un cuadro de diálogo para seleccionar el directorio donde se guardará el documento
        root = tk.Tk()
        root.withdraw()  # Oculta la ventana de Tkinter
        save_path = filedialog.askdirectory()  # Abre el cuadro de diálogo

        # Guarda el documento en el directorio seleccionado
        doc.save(os.path.join(save_path, f'{self.numjui} {self.nombTribunal} {self.fechaNotificacion}.docx'))

        logging.info(f'A estampado {numjui}-{encargo}') 

    def busquedaN(self,row):

        fechaNotificacion = self.table.item(row, 0).text()
        numjui = self.table.item(row, 1).text()  
        nombTribunal = self.table.item(row, 2).text()  
        nombdemandante = self.table.item(row, 3).text()
        apellidemandante = self.table.item(row, 4).text()  
        demandado = self.table.item(row, 5).text()  
        repre = self.table.item(row, 6).text()  
        mandante = self.table.item(row, 7).text()  
        domicilio = self.table.item(row, 8).text()  
        comuna = self.table.item(row, 9).text()  
        encargo = self.table.item(row, 10).text() 
        soli = self.table.item(row, 11).text() 
        arancel = self.table.item(row, 12).text() 

        # Variables de tiempo
        now = datetime.now()
        años = now.strftime("%d/%m/%y")
        horas = now.strftime("%H:%M")

        # Crea un nuevo documento de Word
        doc = Document()

        # Agrega el encabezado con los marcadores de posición
        encabezado = f"{nombTribunal}\n{numjui}  :  {encargo}\n {nombdemandante} {apellidemandante} CON {demandado}"
        doc.add_paragraph(encabezado)

        # Agrega la sección de búsqueda negativa con los datos proporcionados
        busquedaN = f"BÚSQUEDA Y NOTIFICACIÓN: a {años}, siendo las {horas} horas, en su domicilio ubicado en {domicilio} {comuna}, busqué a {demandado}, a fin de notificarle la resolución de fecha **, junto al escrito que antecede, diligencia que no se llevó a efecto por no ser habido en dicho domicilio, en ese momento. Informado por **, quien manifestó que es el domicilio del demandado y que se encuentra en el lugar del juicio, acto seguido procedo a notificar de conformidad al artículo 52 c.p.c. la resolución de fecha **, junto al escrito que antecede,  copia integra fue **. DOY FE."
        doc.add_paragraph(busquedaN)

        # Agrega la firma al final del documento
        doc.add_paragraph(f"Drs. {arancel}.-")

        # Abre un cuadro de diálogo para seleccionar el directorio donde se guardará el documento
        root = tk.Tk()
        root.withdraw()  # Oculta la ventana de Tkinter
        save_path = filedialog.askdirectory()  # Abre el cuadro de diálogo

        # Guarda el documento en el directorio seleccionado
        doc.save(os.path.join(save_path, f'{self.numjui} {self.nombTribunal} {self.fechaNotificacion}.docx'))

        logging.info(f'A estampado {numjui}-{encargo}')

    def fuerzapu(self,row):

        fechaNotificacion = self.table.item(row, 0).text()
        numjui = self.table.item(row, 1).text()  
        nombTribunal = self.table.item(row, 2).text()  
        nombdemandante = self.table.item(row, 3).text()
        apellidemandante = self.table.item(row, 4).text()  
        demandado = self.table.item(row, 5).text()  
        repre = self.table.item(row, 6).text()  
        mandante = self.table.item(row, 7).text()  
        domicilio = self.table.item(row, 8).text()  
        comuna = self.table.item(row, 9).text()  
        encargo = self.table.item(row, 10).text() 
        soli = self.table.item(row, 11).text() 
        arancel = self.table.item(row, 12).text() 

        # Variables de tiempo
        now = datetime.now()
        fecha_actual = now.strftime("%d/%m/%Y")
        hora_actual = now.strftime("%H:%M")

        # Crea un nuevo documento de Word
        doc = Document()

        # Agrega el encabezado con los marcadores de posición
        encabezado = f"{nombTribunal}\n{numjui} : {encargo} \n {nombdemandante} {apellidemandante} CON {demandado}"
        doc.add_paragraph(encabezado)

        # Agrega la sección de retiro de vehículo
        retiro_vehiculo_texto = f"En La Serena, a {fecha_actual}, siendo las {hora_actual} horas, me constituí en {domicilio}, comuna de {comuna}, en presencia de **, placa N° **, cumpliendo la resolución de fecha **, para ser RETIRO DE VEHÍCULO CON FUERZA PÚBLICA Y GRUA, correspondiente a:\n"
        retiro_vehiculo_texto += "Tipo vehículo: \nMarca: \nModelo: \nN° motor: \nN° Chassis: \nColor: \nPATENTE: \nPropietario: \nRut: }\n"
        retiro_vehiculo_texto += f"Se retiró ante persona adulta, sexo masculino, de nombre **, Rut.** , en **.\n"
        retiro_vehiculo_texto += f"Se adjuntan fotografías para mayor detalle del vehículo, encontrado en buen estado, se entregó copia del oficio a **, Rut. **. Se hizo entrega del vehículo a la parte demandante en su domicilio ubicado en **-**. DOY FE.-\n"
        retiro_vehiculo_texto += f"DRS. {arancel}."
        doc.add_paragraph(retiro_vehiculo_texto)

        # Abre un cuadro de diálogo para seleccionar el directorio donde se guardará el documento
        root = tk.Tk()
        root.withdraw()  # Oculta la ventana de Tkinter
        save_path = filedialog.askdirectory()  # Abre el cuadro de diálogo

        # Guarda el documento en el directorio seleccionado
        doc.save(os.path.join(save_path, f'{self.numjui} {self.nombTribunal} {self.fechaNotificacion}.docx'))

        logging.info(f'A estampado {numjui}-{encargo}')


    def EMBARGOFRUSTRADO(self, row):
        
        fechaNotificacion = self.table.item(row, 0).text()
        numjui = self.table.item(row, 1).text()  
        nombTribunal = self.table.item(row, 2).text()  
        nombdemandante = self.table.item(row, 3).text()
        apellidemandante = self.table.item(row, 4).text()  
        demandado = self.table.item(row, 5).text()  
        repre = self.table.item(row, 6).text()  
        mandante = self.table.item(row, 7).text()  
        domicilio = self.table.item(row, 8).text()  
        comuna = self.table.item(row, 9).text()  
        encargo = self.table.item(row, 10).text() 
        soli = self.table.item(row, 11).text() 
        arancel = self.table.item(row, 12).text() 

        # Variables de tiempo
        now = datetime.now()
        fecha_actual = now.strftime("%d/%m/%Y")
        hora_actual = now.strftime("%H:%M")

        # Crea un nuevo documento de Word
        doc = Document()

        # Agrega el encabezado con los marcadores de posición
        encabezado = f"{nombTribunal} \n {numjui} : {encargo} \n {nombdemandante} {apellidemandante} CON {demandado}"
        doc.add_paragraph(encabezado)

        # Agrega la sección de acta de embargo frustrado
        acta_embargo_frustrado = f"EMBARGO FRUSTRADO: En {comuna}, a {fecha_actual}, siendo las {hora_actual} horas, me apersoné en el domicilio de {demandado} ubicado en {domicilio}, {comuna}, con el fin de practicar el embargo ordenado en autos.\n"
        acta_embargo_frustrado += "No obstante, no puedo realizar la diligencia, persona adulta, de sexo femenino, permitió el ingreso, sin hacer uso de la fuerza pública, no obstante no pude llevar a efecto la diligencia por cuanto no hay bienes para la traba del embargo. DOY FE.-\n\n"
        acta_embargo_frustrado += f"Drs. {arancel}.-"
        doc.add_paragraph(acta_embargo_frustrado)

        # Abre un cuadro de diálogo para seleccionar el directorio donde se guardará el documento
        root = tk.Tk()
        root.withdraw()  # Oculta la ventana de Tkinter
        save_path = filedialog.askdirectory()  # Abre el cuadro de diálogo

        # Guarda el documento en el directorio seleccionado
        doc.save(os.path.join(save_path, f'{self.numjui} {self.nombTribunal} {self.fechaNotificacion}.docx'))

        logging.info(f'A estampado {numjui}-{encargo}')
     
    def bban(self, row):

        fechaNotificacion = self.table.item(row, 0).text()
        numjui = self.table.item(row, 1).text()  
        nombTribunal = self.table.item(row, 2).text()  
        nombdemandante = self.table.item(row, 3).text()
        apellidemandante = self.table.item(row, 4).text()  
        demandado = self.table.item(row, 5).text()  
        repre = self.table.item(row, 6).text()  
        mandante = self.table.item(row, 7).text()  
        domicilio = self.table.item(row, 8).text()  
        comuna = self.table.item(row, 9).text()  
        encargo = self.table.item(row, 10).text() 
        soli = self.table.item(row, 11).text() 
        arancel = self.table.item(row, 12).text() 

        # Variables de tiempo
        now = datetime.now()
        fecha_actual = now.strftime("%d/%m/%y")
        hora_actual = now.strftime("%H:%M")

        # Crea un nuevo documento de Word
        doc = Document()

        # Agrega el encabezado con los marcadores de posición
        encabezado = f"{nombTribunal}\nROL/RIT: {numjui} \nCARATULADO: {encargo} CON {repre}"
        doc.add_paragraph(encabezado)

        # Agrega la sección de acta de embargo
        acta_embargo = f"ACTA DE EMBARGO: En la Comuna de {comuna}, a {fecha_actual}, siendo las {hora_actual} horas, en su domicilio ubicado en {domicilio}, notifiqué personalmente a {demandado} en representación del Banco **, solicitud y resolución de embargo por la suma de $** en la cuenta a nombre del demandado {demandado}. Le hice entrega de copia íntegra de lo notificado y firmó. La identidad del notificado se estableció por los datos aportados por el mismo. DOY FE.-\n\n"
        acta_embargo += "Señala que existían los dineros _________\nNo existen dineros en la cuenta _________  Cuenta cerrada _______\n"
        acta_embargo += f"Drs. Dist. Loc ${arancel}.-"
        doc.add_paragraph(acta_embargo)

        # Abre un cuadro de diálogo para seleccionar el directorio donde se guardará el documento
        root = tk.Tk()
        root.withdraw()  # Oculta la ventana de Tkinter
        save_path = filedialog.askdirectory()  # Abre el cuadro de diálogo

        # Guarda el documento en el directorio seleccionado
        doc.save(os.path.join(save_path, f'{self.numjui} {self.nombTribunal} {self.fechaNotificacion}.docx'))

        logging.info(f'A estampado {numjui}-{encargo}')

    def embargoauto(self, row):

        fechaNotificacion = self.table.item(row, 0).text()
        numjui = self.table.item(row, 1).text()  
        nombTribunal = self.table.item(row, 2).text()  
        nombdemandante = self.table.item(row, 3).text()
        apellidemandante = self.table.item(row, 4).text()  
        demandado = self.table.item(row, 5).text()  
        repre = self.table.item(row, 6).text()  
        mandante = self.table.item(row, 7).text()  
        domicilio = self.table.item(row, 8).text()  
        comuna = self.table.item(row, 9).text()  
        encargo = self.table.item(row, 10).text() 
        soli = self.table.item(row, 11).text() 
        arancel = self.table.item(row, 12).text() 

        # Variables de tiempo
        now = datetime.now()
        fecha_actual = now.strftime("%d/%m/%y")
        hora_actual = now.strftime("%H:%M")

        # Crea un nuevo documento de Word
        doc = Document()

        # Agrega el encabezado con los marcadores de posición
        encabezado = f"{nombTribunal}\nROL/RIT: {numjui} \nCARATULADO: {encargo} CON {repre}"
        doc.add_paragraph(encabezado)

        # Agrega la sección de acta de embargo
        acta_embargo = f"ACTA DE EMBARGO: En la Comuna de {comuna}, a {fecha_actual}, siendo las {hora_actual} horas, en su domicilio ubicado en {domicilio}, notifiqué personalmente a {demandado} en representación del Banco **, solicitud y resolución de embargo por la suma de $** en la cuenta a nombre del demandado {demandado}. Le hice entrega de copia íntegra de lo notificado y firmó. La identidad del notificado se estableció por los datos aportados por el mismo. DOY FE.-\n\n"
        acta_embargo += "Señala que existían los dineros _________\nNo existen dineros en la cuenta _________  Cuenta cerrada _______\n"
        acta_embargo += f"Drs. Dist. Loc ${arancel}.-"
        doc.add_paragraph(acta_embargo)

        # Abre un cuadro de diálogo para seleccionar el directorio donde se guardará el documento
        root = tk.Tk()
        root.withdraw()  # Oculta la ventana de Tkinter
        save_path = filedialog.askdirectory()  # Abre el cuadro de diálogo

        # Guarda el documento en el directorio seleccionado
        doc.save(os.path.join(save_path, f'{self.numjui} {self.nombTribunal} {self.fechaNotificacion}.docx'))

        logging.info(f'A estampado {numjui}-{encargo}')

    

   
# Ejecuta la función principal
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = DashboardHistorialActuaciones()
    window.show()
    sys.exit(app.exec())

   