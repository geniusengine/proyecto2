import os
import sys
import time
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QTableWidget, \
    QTableWidgetItem, QHeaderView, QCheckBox, QHBoxLayout, QMessageBox, QLabel, QComboBox, QToolButton, QMenu
from PyQt6.QtGui import QColor, QIcon
from PyQt6.QtCore import QDateTime, QTimer, Qt, pyqtSignal
import mysql.connector
from datetime import datetime
import logging
from docx import Document

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
        self.actuar = None
    
    def initUI(self):
        self.setWindowTitle('Historial Actuaciones')
        self.setWindowIcon(QIcon("static/icono-ventana.png"))
        self.setGeometry(100, 100, 1280, 720)

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)
        self.layout_vertical = QVBoxLayout()
        self.layout_horizontal = QHBoxLayout()
   
        self.layout_horizontal.addLayout(self.layout_vertical)

        # Crea una tabla
        self.table = QTableWidget()
        self.table.setStyleSheet(
            "QTableView { gridline-color: white; }"
            "QTableCornerButton::section { background-color: #d3d3d3; border: 1px solid black; }"
            "QHeaderView::section { background-color: #d3d3d3; border: 1px solid black; }"
        )
        self.layout_vertical.addWidget(self.table)
    
        # Conectar la señal de clic en el encabezado de la columna para ordenar
        self.table.horizontalHeader().sectionClicked.connect(self.ordenar_tabla)

        # Configuraciones finales del diseño
        self.central_widget.setLayout(self.layout_horizontal)

        # Conexión y muestra inicial de datos
        self.establecer_conexion_base_de_datos()
        self.obtener_datos()
        self.mostrar_tabla()

        self.setGeometry(100, 100, 400, 300)
    
        # Crear el botón
        self.button = QPushButton('Seleccionar y Guardar', self)
        self.button.clicked.connect(self.confirm_and_save)
        self.layout_vertical.addWidget(self.button)
        self.layout_vertical.setAlignment(self.button, Qt.AlignmentFlag.AlignRight)

        self.show()

    def ordenar_tabla(self, logicalIndex):
        order = self.table.horizontalHeader().sortIndicatorOrder()
        self.table.sortItems(logicalIndex, order)


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
        max_width = 1000
        min_width = min(min_width, max_width)
        
        self.setMinimumWidth(min_width - 260)
        self.setMaximumWidth(max_width)
        self.adjustSize()

    def obtener_datos(self):
        try:
            self.establecer_conexion_base_de_datos()
            cursor = self.db_connection.cursor()
            query = "SELECT fechaNotificacion, numjui, nombTribunal, demandante, demandado, repre, mandante, domicilio, comuna, encargo, soli, arancel, estadoNoti, estadoCausa, actu FROM AUD_notificacion"
            cursor.execute(query)
            resultados = cursor.fetchall()
            self.causas = []
            for fila in resultados:
                causa = {'fechaNotificacion': fila[0], 'numjui': fila[1], 'nombtribunal': fila[2], 'demandante': fila[3], 'demandado': fila[4],
                         'repre': fila[5], 'mandante': fila[6], 'domicilio': fila[7], 'comuna': fila[8], 'encargo': fila[9], 'soli': fila[10],
                         'arancel': fila[11], 'actuacion': 'actuacion'}
                self.causas.append(causa)
        except mysql.connector.Error as e:
            print(f"Error al acceder a la base de datos: {e}")
        finally:
            self.cerrar_conexion_base_de_datos()

    def mostrar_tabla(self):
        self.table.setColumnCount(13)
        self.table.setHorizontalHeaderLabels(['fechaNotificacion', 'Rol', 'Tribunal', 'demandante', 'demandado', 'Representante', 'Mandante', 'Domicilio', 'Comuna', 'Encargo', 'Resultado', 'Arancel', 'Actuación'])
        for row_index, causa in enumerate(self.causas):
            self.table.insertRow(row_index)
            for col_index, (key, value) in enumerate(causa.items()):
                if key == "actuacion":
                    combo_box = QComboBox()
                    opciones_actuaciones = ["Elija actuación", "Búsqueda Negativa", "Búsqueda Positiva", "Not. por cédula", "Not. Art. 44", "Req. de pago en Oficina", "Op. al Embargo", "Not. Personal", "Not. Personal/Req. de Pago", "Not. art. 52", "Embargo con Fuerza Pública", "Embargo Frustrado", "Embargo Banco", "Embargo Vehículo", "Retiro de Vehículo", "Retiro Frustrado", "Retiro de Especies ", "OtrO"]
                    combo_box.addItems(opciones_actuaciones)
                    combo_box.setCurrentText(value)
                    self.table.setCellWidget(row_index, col_index, combo_box)
                    combo_box.currentIndexChanged.connect(lambda index, row=row_index, col=col_index: self.combo_box_changed(row, col, index))
                else:
                    item = QTableWidgetItem(str(value))
                    item.setBackground(QColor(52, 152, 219))
                    self.table.setItem(row_index, col_index, item)
        self.ajustar_tamanio()

    def combo_box_changed(self, row, col, index):
        combo_box = self.table.cellWidget(row, col)
        selected_value = combo_box.currentText()
        self.actuar = selected_value
        print(f"Valor seleccionado: {selected_value}")

    def confirm_and_save(self):
        selected_row = self.table.currentRow()
        if selected_row >= 0:
            data_to_save = tuple([self.table.item(selected_row, col).text() if self.table.item(selected_row, col) is not None else '' for col in range(14)])
            fecha_notificacion = datetime.strptime(data_to_save[0], '%Y-%m-%d %H:%M:%S.%f').strftime('%Y-%m-%d %H:%M:%S')
            data_to_save = (fecha_notificacion,) + data_to_save[1:]
            reply = QMessageBox.question(self, 'Confirmar', f'Seguro que quieres devolver estos datos?\n{data_to_save}',
                                         QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)

            if reply == QMessageBox.StandardButton.Yes:
                actuacion = self.actuar
                self.establecer_conexion_base_de_datos()
                cursor = self.db_connection.cursor()
                cursor.execute('INSERT INTO notificacion (fechaNotificacion, numjui, nombTribunal, demandante, demandado, repre, mandante, domicilio, comuna, encargo, soli, arancel, estadoNoti, estadoCausa, actu) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)', data_to_save + (actuacion,))
                self.db_connection.commit()
                print('Datos guardados en la tabla de notificaciones')
                self.cerrar_conexion_base_de_datos()

# Función principal
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = DashboardHistorialActuaciones()
    window.show()
    sys.exit(app.exec())
