import sys
import time
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QTableWidget, \
    QTableWidgetItem, QHeaderView, QCheckBox, QHBoxLayout , QMessageBox, QLabel,QComboBox
from PyQt6.QtGui import QColor, QIcon
from PyQt6.QtCore import QDateTime, QTimer, Qt, pyqtSignal
import pymssql


from funcionalidades.estampado_app import Estampadoxd
import logging

# Configurar el sistema de registro
logging.basicConfig(filename='registro.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


class Dashboard_actuacionesApp(QMainWindow):
    def __init__(self,numjui, nombTribunal, fecha):
        self.numjui = numjui
        self.nombTribunal = nombTribunal
        self.fecha = fecha

        super().__init__()
        self.db_connection = None
        self.initUI()
        print("Dashboard Actuaciones")
    
    def initUI(self):
        self.setWindowTitle('Dashboard App')
        self.setWindowIcon(QIcon("static/icono-ventana.png"))
        self.setGeometry(100, 100, 1280, 720)

        # Agrega un botón para guardar datos
        self.save_button = QPushButton("Guardar Datos")
        self.save_button.clicked.connect(self.guardar_datos)

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)
        self.layout_vertical = QVBoxLayout()  # Crea un layout vertical
        self.layout_horizontal = QHBoxLayout()  # Crea un layout horizontal
   
        self.layout_horizontal.addLayout(self.layout_vertical)# Agrega el layout vertical al layout horizontal
        self.layout_horizontal.addWidget(self.save_button)# Agrega el botón de guardar al layout horizontal

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
        self.mostrar_tabla()

        self.setGeometry(100, 100, 400, 300)
    def guardar_datos(self):
        print ("Guardando datos...")
        # Lógica para guardar datos desde la tabla
        db_connection = pymssql.connect(
            server='vps-3697915-x.dattaweb.com',
            user='daniel',
            password='LOLxdsas--',
            database='micau5a')
        try:
            cursor = db_connection.cursor()
            insert_query = "INSERT INTO actuaciones (numjui, nombTribunal, tipojuicio,actuacion,fecha) VALUES (%s, %s, %s, %s, %s)"
            cursor.execute(insert_query, (self.numjui, self.nombTribunal, self.tipojuicio, self.actuacion, self.fecha))
            db_connection.commit()
            db_connection.close()
            QMessageBox.information(self, "Éxito", "Datos guardados correctamente")

            logging.info(f'Insercion-seguimiento de causa {self.numjui}-{self.nombTribunal}')

        except Exception as e:
            print(e)
            QMessageBox.critical(self, "Error", "Error al guardar los datos")
            db_connection.rollback()# Limpia la tabla

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
        max_width = 800  # Puedes ajustar este valor según tus necesidades
        min_width = min(min_width, max_width)
        
        self.setMinimumWidth(min_width - 375)
        self.setMaximumWidth(max_width)  # Establecer un ancho máximo para la ventana
        self.adjustSize()
# muestra los datos en la tabla
    def mostrar_tabla(self):
        causa = {"fecha": self.fecha,
                "numjui": self.numjui,
                "tribunal": self.nombTribunal,
                "actuacion": "Actuacionprueba",
                "tipojuicio": "Tipojuicioprueba",
                "Estampada": "Estampada"}
        print(causa)
        self.causas = []
        self.causas.append(causa)
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(['Fecha',  'Rol', 'Tribunal','Actuacion','Tipo de juicio','Estampar'])
        for row_index, causa in enumerate(self.causas):
            self.table.insertRow(row_index)
            for col_index, (key, value) in enumerate(causa.items()):
                if key == "Estampada":
                    button = self.crear_boton_con_icono("static/firmar.png", self.estampar_clicked)
                    self.table.setCellWidget(row_index, col_index, button)
                elif key == "actuacion":
                    # Crear un objeto QComboBox para las celdas de actuaciones
                    combo_box = QComboBox()
                    opciones_actuaciones = ["Elija actuacion","Búsqueda Negativa","Búsqueda Positiva","Not. por cédula","Not. Art. 44" ,"Req. de pago en Oficina", "Op. al Embargo" ,"Not. Personal" ,"Not. Personal/ Req. de Pago" ,"Not. art. 52" ,"Embargo con Fuerza Pública" ,"Embargo Frustrado" ,"Embargo Banco" ,"Embargo Vehículo" ,"Retiro de Vehículo" ,"Retiro Frustrado" ,"Retiro de Especies "  ,"OtrO"  ]  # Puedes personalizar las opciones
                    combo_box.addItems(opciones_actuaciones)
                    combo_box.setCurrentText(value)
                    self.table.setCellWidget(row_index, col_index, combo_box)
                    combo_box.currentIndexChanged.connect(lambda index, row=row_index, col=col_index: self.combo_box_changed(row, col, index))# obtiene el valor del combo box seleccionado
                elif key == "tipojuicio":
                    # Crear un objeto QComboBox para las celdas de tipo de juicio
                    combo_box = QComboBox()
                    opciones_tipojuicio = ["Elija tipo de juicio","Ejecutivo", "Ordinario"]
                    combo_box.addItems(opciones_tipojuicio)
                    combo_box.setCurrentText(value)
                    self.table.setCellWidget(row_index, col_index, combo_box)
                    combo_box.currentIndexChanged.connect(lambda index, row=row_index, col=col_index: self.combo_box_changed(row, col, index))
                else:
                    # Crea un objeto QTableWidgetItem para las otras columnas
                    item = QTableWidgetItem(str(value))
                    #establece el color de la celda
                    item.setBackground(QColor(26, 26, 255))
                    self.table.setItem(row_index, col_index, item)  
                    print(key, value)
        self.ajustar_tamanio()
    
    def combo_box_changed(self, row, col, index):
        # Esta función se llama cuando cambia la selección en un QComboBox
        combo_box = self.table.cellWidget(row, col)
        selected_value = combo_box.currentText()
        if col == 3:  # Col 3 es la columna de actuación
            self.actuacion = selected_value
        elif col == 4:  # Col 4 es la columna de tipo de juicio
            self.tipojuicio = selected_value

        print(f"En la fila {row}, columna {col}, se seleccionó: {selected_value}")
# Función para ordenar la tabla según la columna clicada
    def ordenar_tabla(self, logicalIndex):
        self.table.sortItems(logicalIndex, Qt.SortOrder.AscendingOrder if self.table.horizontalHeader().sortIndicatorOrder() == Qt.SortOrder.DescendingOrder else Qt.SortOrder.DescendingOrder)

    def obtener_datos_causa(self, numjui):
        try:
            with self.db_connection.cursor() as cursor:
                query = "SELECT nombTribunal, nombdemandante, apellidemandante, demandado, repre, mandante, domicilio, comuna, encargo, soli, arancel FROM AUD_notificacion WHERE numjui = %s"
                cursor.execute(query, (numjui,))
                resultado = cursor.fetchone()

            if resultado:
                return resultado
            else:
                return None
        except Exception as e:
            print(f"Error al obtener datos de la base de datos: {e}")
            return None
        
# abre la ventana de estampado
    def estampar_clicked(self):
        # Obtener la fila seleccionada
        selected_row = self.table.currentRow()
        # Verificar si se seleccionó una fila
        if selected_row != -1:
        # Obtener datos de la fila seleccionada
            numjui = self.table.item(selected_row, 1).text()

            # Recuperar datos de la base de datos para el numjui seleccionado
            datos_causa = self.obtener_datos_causa(numjui)

            # Verificar si se recuperaron los datos
            if datos_causa:
                # Desempaquetar los datos recuperados
                nombTribunal, nombdemandante, apellidemandante, demandado, repre, mandante, domicilio, comuna, encargo, soli, arancel = datos_causa

                # Importar Estampadoxd localmente
                self.ex3 = Estampadoxd(numjui, nombTribunal, nombdemandante, apellidemandante, demandado, repre, mandante, domicilio, comuna, encargo, soli, arancel)
                self.ex3.show()
            else:
                QMessageBox.warning(self, "Advertencia", f"No puede estampar datos, datos no encontrados {numjui}.")
        
        button = self.sender()
        index = self.table.indexAt(button.pos())
        row, col = index.row(), index.column()
        causa = self.causas[row]
        color = QColor(250, 193, 114)

        # Verifica si la causa ya ha sido notificada
        if causa["Estampada"] == 1:
            return
        
        # Actualiza la información localmente
        causa["Estampada"] = 1
        
        # Actualiza el valor en la base de datos
        try:
            self.establecer_conexion_base_de_datos()
            with self.db_connection.cursor() as cursor:
                query = "UPDATE AUD_notificacion SET estadoCausa = 1 WHERE numjui = %s"
                cursor.execute(query, (causa['numjui'],))
            self.db_connection.commit()
        except pymssql.Error as db_error:
            print(f"Error al ejecutar la consulta SQL: {db_error}")
            self.db_connection.rollback()
            raise  # Re-levanta la excepción para que el programa no continúe si hay un error grave en la base de datos
        except Exception as e:
            print(f"Error desconocido: {e}")
            raise  # Re-levanta la excepción para que el programa no continúe si hay un error desconocido
        finally:
            self.cerrar_conexion_base_de_datos()
        # Actualiza la celda en la tabla y el color de la fila
        self.actualizar_color_fila(row)
        # Proporciona un mensaje de éxito al usuario

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
     # función para actualizar el color de la fila
    def actualizar_color_fila(self, row):
        causa = self.causas_seleccionadas[row]
        print(causa)
        #notificada = causa["Notificada"]
        estampada = causa["estadoCausa"]
        
        for col_index in range(self.table.columnCount()):
            item = self.table.item(row, col_index)
            if item is not None:
                # Llamas a la función que establece el color para cada celda
                self.color_y_etiqueta_celda(item, estampada)

        # Actualiza la vista de la tabla
        self.table.viewport().update()
# Función principal
# Ejecuta la función principal
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Dashboard_actuacionesApp()
    window.show()
    sys.exit(app.exec())

   