import mysql.connector
import subprocess
import sys
from PyQt6.QtGui import QColor, QIcon
from PyQt6.QtWidgets import QMessageBox, QApplication, QRadioButton, QButtonGroup, QMainWindow, QPushButton, QLabel, QLineEdit, QTableWidgetItem, QVBoxLayout, QHBoxLayout, QWidget, QCheckBox, QTableWidget
from PyQt6.QtCore import Qt

import logging

# Configurar el sistema de registro
logging.basicConfig(filename='registro.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class BuscadorDatosCausaApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Buscador de Datos de Causa")
        self.setWindowIcon(QIcon("static/icono-ventana.png"))
        self.setGeometry(100, 100, 600, 400)
        self.initUI()

    def initUI(self):
        main_layout = QVBoxLayout()
        search_layout = QHBoxLayout()

        # Campos de búsqueda
        self.check_numjui = QCheckBox("Rol")
        self.numjui_input = QLineEdit(self)
        self.check_tribunal = QCheckBox("Tribunal")
        self.tribunal_input = QLineEdit(self)

        search_layout.addWidget(self.check_numjui)
        search_layout.addWidget(self.numjui_input)
        search_layout.addWidget(self.check_tribunal)
        search_layout.addWidget(self.tribunal_input)

        self.button_search = QPushButton("Buscar", self)
        self.button_search.clicked.connect(self.search_data)
        search_layout.addWidget(self.button_search)
        main_layout.addLayout(search_layout)

        # Tabla de resultados
        self.table = QTableWidget()
        main_layout.addWidget(self.table)
        self.checkbox_group = QButtonGroup()
        self.checkbox_group.setExclusive(True)
        self.checkbox_group.buttonToggled.connect(self.checkbox_seleccionado)

        self.causa_seleccionada = []
        self.result_checkboxes = []

        # Botones de acción
        self.buttons_layout = QHBoxLayout()
        self.button_select = QPushButton("Seleccionar", self)
        self.button_select.clicked.connect(self.select_results)
        self.buttons_layout.addWidget(self.button_select)

        self.button_clear = QPushButton("Limpiar", self)
        self.button_clear.clicked.connect(self.limpiar_tabla)
        self.buttons_layout.addWidget(self.button_clear)

        main_layout.addLayout(self.buttons_layout)
        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

    def limpiar_tabla(self):
        self.table.clearContents()
        self.table.setRowCount(0)

    def establecer_conexion_base_de_datos(self):
        self.db_connection = mysql.connector.connect(
            host='causas.mysql.database.azure.com', 
            user='admin_carlos',
            password='F14tomcat',
            database='matias1'
        )

    def cerrar_conexion_base_de_datos(self):
        if self.db_connection:
            self.db_connection.close()

    def search_data(self):
        search_by_numjui = self.check_numjui.isChecked()
        search_by_tribunal = self.check_tribunal.isChecked()
        numjui = self.numjui_input.text()
        tribunal = self.tribunal_input.text()

        if not search_by_numjui and not search_by_tribunal:
            print("No se ha seleccionado ningún criterio de búsqueda.")
            return

        try:
            self.establecer_conexion_base_de_datos()
            cursor = self.db_connection.cursor()
            
            if search_by_numjui:
                query = "SELECT fechaNotificacion, numjui, nombTribunal FROM buscar_historico WHERE numjui = %s"
                cursor.execute(query, (numjui,))
            elif search_by_tribunal:
                query = "SELECT fechaNotificacion, numjui, nombTribunal FROM buscar_historico WHERE nombtribunal = %s"
                cursor.execute(query, (tribunal,))
            elif search_by_numjui and search_by_tribunal:
                query = "SELECT fechaNotificacion, numjui, nombTribunal FROM buscar_historico WHERE numjui = %s OR nombtribunal = %s"
                cursor.execute(query, (numjui, tribunal))

            resultado = cursor.fetchall()
            self.cerrar_conexion_base_de_datos()
            self.limpiar_tabla()
            
            if resultado:
                self.table.setStyleSheet(
                    "QTableView { gridline-color: grey; }"
                    "QTableCornerButton::section { background-color: #d3d3d3; border: 1px solid black; }"
                    "QHeaderView::section { background-color: #d3d3d3; border: 1px solid black; }"
                    "QTableWidget::item {padding: 5px;text-align: center;}"
                )
                self.causas = []
                for fila in resultado:
                    fecha_formateada = fila[0].strftime("%d-%m-%Y")
                    causa = {
                        "fecha Notificacion": fecha_formateada,
                        "rol": fila[1],
                        "tribunal": fila[2],
                        "checkbox": "",
                    }
                    self.causas.append(causa)

                self.table.setColumnCount(4)
                self.table.setHorizontalHeaderLabels(['Fecha', 'Rol', 'Tribunal', 'Seleccionar'])
                for row_index, causa in enumerate(self.causas):
                    self.table.insertRow(row_index)
                    for column_index, (key, value) in enumerate(causa.items()):
                        if key == "checkbox":
                            checkbox = QRadioButton()
                            self.checkbox_group.addButton(checkbox)
                            self.table.setCellWidget(row_index, column_index, checkbox)
                        item = QTableWidgetItem(str(value))  
                        self.table.setItem(row_index, column_index, item)
            else:
                self.limpiar_tabla()
                self.table.setColumnCount(1)
                self.table.setHorizontalHeaderLabels(['No se encontraron datos para la búsqueda especificada.'])
                print("No hay datos")
        except mysql.connector.Error as err:
            self.limpiar_tabla()
            self.table.setColumnCount(1)
            self.table.setHorizontalHeaderLabels([str(err)])  
            print("Error al buscar:", err)
        self.ajustar_tamanio()

    def ajustar_tamanio(self):
        self.table.resizeColumnsToContents()
        total_width = sum(self.table.columnWidth(col) for col in range(self.table.columnCount()))
        min_width = max(self.width(), total_width)
        self.setMinimumWidth(min_width + 40)
        self.adjustSize()

    def checkbox_seleccionado(self, checkbox, checked):
        if checked:
            row_index = self.table.indexAt(checkbox.pos()).row()
            cols = self.table.columnCount()
            self.causa_seleccionada = [self.table.item(row_index, col).text() for col in range(cols)]

    def select_results(self):
        if not self.causa_seleccionada:
            QMessageBox.warning(self, "Advertencia", "No se ha seleccionado ningún resultado para mostrar.")
            return
        
        self.limpiar_tabla()
        self.table.setColumnCount(15)
        self.table.setHorizontalHeaderLabels(['Fecha', 'Rol', 'Tribunal', 'Demandante', 'Demandando', 'Representante', 'Mandante', 'Domicilio', 'Comuna', 'Encargo', 'Solicitud', 'Arancel', 'Actuacion', 'Notificar', 'Estampar'])
        
        try:
            self.establecer_conexion_base_de_datos()
            cursor = self.db_connection.cursor()

            numjui = self.causa_seleccionada[1]
            query = "SELECT fechaNotificacion, numjui, nombTribunal, demandante, demandado, repre, mandante, domicilio, comuna, encargo, soli, arancel, estadoNoti, estadoCausa, actu FROM buscar_historico WHERE numjui = %s"
            cursor.execute(query, (numjui,))
            causas = cursor.fetchall()
            self.cerrar_conexion_base_de_datos()

            if causas:
                for row_index, fila in enumerate(causas):
                    fecha_formateada = fila[0].strftime("%d-%m-%Y")
                    datos_causa = {
                        "Fecha notificacion": fecha_formateada,
                        "Rol": fila[1],
                        "Tribunal": fila[2],
                        "Demandante": fila[3],
                        "Demandado": fila[4],
                        "Representante": fila[5],
                        "Mandante": fila[6],
                        "Domicilio": fila[7],
                        "Comuna": fila[8],
                        "Encargo": fila[9],
                        "Solicitud": fila[10],
                        "Arancel": fila[11],
                        "Notificar": "Notificar",
                        "Estampar": "Estampar",
                        "estadoCausa": fila[13],
                    }
                    for col_index, (key, value) in enumerate(datos_causa.items()):
                        item = QTableWidgetItem(str(value) if key != "checkbox" else "")
                        self.table.setItem(row_index, col_index, item)

        except mysql.connector.Error as err:
            print("Error al buscar datos detallados:", err)

    def color_y_etiqueta_celda(self, item, notificada, estampada):
        if item:
            color = QColor(250, 193, 114)
            if notificada and estampada:
                color = QColor(46, 204, 113)  # Verde
            elif not notificada and estampada:
                color = QColor(250, 193, 114)  # Amarillo
            elif not notificada and not estampada:
                color = QColor(224, 92, 69)  # Rojo
            item.setBackground(color)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = BuscadorDatosCausaApp()
    window.show()
    sys.exit(app.exec())
