import sys
import time
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QTableWidget, \
    QTableWidgetItem, QHeaderView, QCheckBox, QHBoxLayout, QMessageBox, QLabel, QComboBox
from PyQt6.QtGui import QColor, QIcon
from PyQt6.QtCore import QDateTime, QTimer, Qt, pyqtSignal
import mysql.connector
import logging

from funcionalidades.estampado_app import Estampadoxd

# Configurar el sistema de registro
logging.basicConfig(filename='registro.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


class Dashboard_actuacionesApp(QMainWindow):
    def __init__(self, numjui, nombTribunal, fecha):
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
        self.layout_vertical = QVBoxLayout()
        self.layout_horizontal = QHBoxLayout()
   
        self.layout_horizontal.addLayout(self.layout_vertical)
        self.layout_horizontal.addWidget(self.save_button)

        # Crea una tabla
        self.table = QTableWidget()
        self.table.setStyleSheet(
            "QTableView { gridline-color: white; }"
            "QTableCornerButton::section { background-color: #d3d3d3; border: 1px solid black; }"
            "QHeaderView::section { background-color: #d3d3d3; border: 1px solid black; }"
        )
        self.layout_vertical.addWidget(self.table)
    
        self.table.horizontalHeader().sectionClicked.connect(self.ordenar_tabla)

        self.central_widget.setLayout(self.layout_horizontal)

        # Conexión y muestra inicial de datos
        self.establecer_conexion_base_de_datos()
        self.mostrar_tabla()

        self.setGeometry(100, 100, 400, 300)

    def verificar_numjui_en_demanda(self):
        cursor = self.db_connection.cursor()
        query = "SELECT COUNT(*) FROM demanda WHERE numjui = %s"
        cursor.execute(query, (self.numjui,))
        resultado = cursor.fetchone()
        return resultado[0] > 0


    def guardar_datos(self):
        if not self.verificar_numjui_en_demanda():
            QMessageBox.warning(self, "Error", f"El numjui '{self.numjui}' no existe en la tabla 'demanda'.")
            return

        try:
            db_connection = mysql.connector.connect(
                host='causas.mysql.database.azure.com', 
                user='admin_carlos',
                password='F14tomcat',
                database='matias1'
            )
            cursor = db_connection.cursor()
            insert_query = "INSERT INTO actuaciones (numjui, nombTribunal, tipojuicio, actuacion, fecha) VALUES (%s, %s, %s, %s, %s)"
            cursor.execute(insert_query, (self.numjui, self.nombTribunal, self.tipojuicio, self.actuacion, self.fecha))
            db_connection.commit()
            QMessageBox.information(self, "Éxito", "Datos guardados correctamente")
            logging.info(f'Insercion-seguimiento de causa {self.numjui}-{self.nombTribunal}')
        except mysql.connector.Error as e:
            print(e)
            QMessageBox.critical(self, "Error", "Error al guardar los datos")
            db_connection.rollback()


    def crear_boton(self, texto, funcion):
        boton = QPushButton(texto, self)
        boton.clicked.connect(funcion)
        return boton

    def crear_boton_con_icono(self, icono_path, funcion):
        boton = QPushButton(self)
        icono = QIcon(icono_path)
        boton.setIcon(icono)
        boton.clicked.connect(funcion)
        return boton
    
    def establecer_conexion_base_de_datos(self):
        try:
            self.db_connection = mysql.connector.connect(
                host='causas.mysql.database.azure.com', 
                user='admin_carlos',
                password='F14tomcat',
                database='matias1'
            )
            if self.db_connection.is_connected():
                print("Conexión a la base de datos MySQL establecida.")
        except mysql.connector.Error as e:
            print(f"Error al conectar a la base de datos MySQL: {e}")
            sys.exit(1)

    def cerrar_conexion_base_de_datos(self):
        if self.db_connection.is_connected():
            self.db_connection.close()

    def limpiar_tabla(self):
        self.table.clearContents()
        self.table.setRowCount(0)

    def ajustar_tamanio(self):
        self.table.resizeColumnsToContents()
        total_width = sum(self.table.columnWidth(col) for col in range(self.table.columnCount()))
        min_width = max(self.width(), total_width)
        max_width = 800
        min_width = min(min_width, max_width)
        
        self.setMinimumWidth(min_width - 375)
        self.setMaximumWidth(max_width)
        self.adjustSize()

    def mostrar_tabla(self):
        causa = {
            "fecha": self.fecha,
            "numjui": self.numjui,
            "tribunal": self.nombTribunal,
            "actuacion": "Actuacionprueba",
            "tipojuicio": "Tipojuicioprueba"
        }
        print(causa)
        self.causas = [causa]
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(['Fecha', 'Rol', 'Tribunal', 'Actuacion', 'Tipo de juicio'])
        for row_index, causa in enumerate(self.causas):
            self.table.insertRow(row_index)
            for col_index, (key, value) in enumerate(causa.items()):
                if key == "actuacion":
                    combo_box = QComboBox()
                    opciones_actuaciones = ["Elija actuacion", "Búsqueda Negativa", "Búsqueda Positiva", "Not. por cédula", "Not. Art. 44", "Req. de pago en Oficina", "Op. al Embargo", "Not. Personal", "Not. Personal/Req. de Pago", "Not. art. 52", "Embargo con Fuerza Pública", "Embargo Frustrado", "Embargo Banco", "Embargo Vehículo", "Retiro de Vehículo", "Retiro Frustrado", "Retiro de Especies", "Otro"]
                    combo_box.addItems(opciones_actuaciones)
                    combo_box.setCurrentText(value)
                    self.table.setCellWidget(row_index, col_index, combo_box)
                    combo_box.currentIndexChanged.connect(lambda index, row=row_index, col=col_index: self.combo_box_changed(row, col, index))
                elif key == "tipojuicio":
                    combo_box = QComboBox()
                    opciones_tipojuicio = ["Elija tipo de juicio", "Ejecutivo", "Ordinario"]
                    combo_box.addItems(opciones_tipojuicio)
                    combo_box.setCurrentText(value)
                    self.table.setCellWidget(row_index, col_index, combo_box)
                    combo_box.currentIndexChanged.connect(lambda index, row=row_index, col=col_index: self.combo_box_changed(row, col, index))
                else:
                    item = QTableWidgetItem(str(value))
                    item.setBackground(QColor(26, 26, 255))
                    self.table.setItem(row_index, col_index, item)  
                    print(key, value)
        self.ajustar_tamanio()

    def combo_box_changed(self, row, col, index):
        combo_box = self.table.cellWidget(row, col)
        selected_value = combo_box.currentText()
        if col == 3:
            self.actuacion = selected_value
        elif col == 4:
            self.tipojuicio = selected_value
        print(f"En la fila {row}, columna {col}, se seleccionó: {selected_value}")

    def ordenar_tabla(self, logicalIndex):
        self.table.sortItems(logicalIndex, Qt.SortOrder.AscendingOrder if self.table.horizontalHeader().sortIndicatorOrder() == Qt.SortOrder.DescendingOrder else Qt.SortOrder.DescendingOrder)

    def obtener_datos_causa(self, numjui):
        try:
            cursor = self.db_connection.cursor()
            query = "SELECT nombTribunal, demandante, demandado, repre, mandante, domicilio, comuna, encargo, soli, arancel FROM AUD_notificacion WHERE numjui = %s"
            cursor.execute(query, (numjui,))
            resultado = cursor.fetchone()
            return resultado if resultado else None
        except mysql.connector.Error as e:
            print(f"Error al obtener datos de la base de datos: {e}")
            return None

    def estampar_clicked(self):
        selected_row = self.table.currentRow()
        if selected_row != -1:
            numjui = self.table.item(selected_row, 1).text()
            datos_causa = self.obtener_datos_causa(numjui)

            if datos_causa:
                nombTribunal, demandante, demandado, repre, mandante, domicilio, comuna, encargo, soli, arancel = datos_causa
                self.ex3 = Estampadoxd(numjui, nombTribunal, demandante, demandado, repre, mandante, domicilio, comuna, encargo, soli, arancel)
                self.ex3.show()
            else:
                QMessageBox.warning(self, "Advertencia", f"No puede estampar datos, datos no encontrados {numjui}.")

# Función principal
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Dashboard_actuacionesApp(numjui="12345", nombTribunal="Tribunal", fecha="2024-10-30")
    window.show()
    sys.exit(app.exec())
