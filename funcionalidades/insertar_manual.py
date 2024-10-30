import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QTableWidget, QTableWidgetItem, QPushButton, QWidget, QMessageBox, QHBoxLayout, QComboBox, QLineEdit
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QIcon
from datetime import datetime
import mysql.connector
import logging
from .dashboard_actuaciones import Dashboard_actuacionesApp
from .estampado_app import Estampadoxd

# Configurar el sistema de registro
logging.basicConfig(filename='registro.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class MiApp(QMainWindow):
    def __init__(self):
        self.nombTribunal = None
        datos_guardados_signal = pyqtSignal()
        super().__init__()

        # Inicializa un diccionario para almacenar las selecciones de combo box
        self.selecciones_combo_box = {}
        self.actu_sec_combo_box = {}

        self.setWindowTitle("Ingreso de Datos")
        self.setWindowIcon(QIcon("static/icono-ventana.png"))
        self.setGeometry(100, 100, 800, 400)

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        layout = QHBoxLayout()
        layout_vertical = QVBoxLayout()
        
        self.table = QTableWidget()
        self.table.setColumnCount(12)
        self.table.setHorizontalHeaderLabels(['Rol', 'Tribunal', 'Demandante', 'Demandando', 'Representante', 'Mandante', 'Domicilio', 'Comuna', 'Encargo', 'Resultado', 'Arancel', 'Actuacion'])
        layout.addWidget(self.table)

        self.add_row_button = QPushButton("Agregar Fila")
        self.add_row_button.clicked.connect(self.add_row)
        layout_vertical.addWidget(self.add_row_button)

        self.delete_row_button = QPushButton("Eliminar Fila")
        self.delete_row_button.clicked.connect(self.delete_row)
        layout_vertical.addWidget(self.delete_row_button)

        self.save_button = QPushButton("Guardar Datos")
        self.save_button.clicked.connect(self.save_data)
        layout_vertical.addWidget(self.save_button)

        layout.addLayout(layout_vertical)
        self.central_widget.setLayout(layout)
        self.ajustar_tamanio()

        # Conecta el evento itemChanged a la función de validación
        self.table.itemChanged.connect(self.validar_arancel)

    def validar_arancel(self, item):
        # Verifica si la columna es la correspondiente a arancel
        if item.column() == 10:
            # Verifica si el contenido no es un número
            if not item.text().replace('.', '', 1).isdigit():
                QMessageBox.warning(self, "Advertencia", "Solo se permiten números en la celda de Arancel.")
                item.setText("0")  # Establece un valor predeterminado si no es un número

    def add_row(self):
        self.table.insertRow(self.table.rowCount())
        tribunal_combobox = QComboBox()
        tribunal_combobox.addItems(['1° Juzgado de Letras La Serena',
                                    '2° Juzgado de Letras La Serena',
                                    '3° Juzgado de Letras La Serena',
                                    '1° Juzgado de Letras Coquimbo',
                                    '2° Juzgado de Letras Coquimbo',
                                    '3° Juzgado de Letras Coquimbo',
                                    'Juzgado de Letras del Trabajo de La Serena',
                                    'Juzgado de Garantía La Serena',
                                    'Juzgado de Juicio Oral en lo Penal La Serena',
                                    'Juzgado de Familia La Serena',
                                    'Juzgado de Familia Coquimbo',
                                    'Corte de Apelaciones de La Serena'])
        
        actuacion_combobox = QComboBox()
        actuacion_combobox.addItems(['Búsqueda Negativa', 'Búsqueda Positiva', 'Not. por cédula', 
                                     'Not. Art. 44', 'Req. de pago en Oficina', 'Op. al Embargo', 
                                     'Not. Personal', 'Not. Personal/Req. de Pago', 'Not. art. 52', 
                                     'Embargo con Fuerza Pública', 'Embargo Frustrado', 'Embargo Banco', 
                                     'Embargo Vehículo', 'Embargo TGR', 'Op.Retiro', 'Retiro de Vehículo',
                                     'In.Vehiculo', 'Not. Martillero', 'Retiro Frustrado', 'Retiro de Especies',
                                     'Retiro fuerza pública', 'Otro'])

        # Configura el nuevo QComboBox en la celda correspondiente
        item = QTableWidgetItem()
        self.table.setItem(self.table.rowCount() - 1, 1, item)
        self.table.setItem(self.table.rowCount() - 1, 11, item)

        self.table.setCellWidget(self.table.rowCount() - 1, 1, tribunal_combobox)
        self.table.setCellWidget(self.table.rowCount() - 1, 11, actuacion_combobox)

        tribunal_combobox.currentIndexChanged.connect(lambda index, row=self.table.rowCount()-1, col=1: self.combo_box_changed(row, col, index))
        actuacion_combobox.currentIndexChanged.connect(lambda index, row=self.table.rowCount()-1, col=11: self.actuacion_combobox_changed(row, col, index))

    def combo_box_changed(self, row, col, index):
        combo_box = self.table.cellWidget(row, col)
        selected_value = combo_box.currentText()
        self.selecciones_combo_box[(row, col)] = selected_value

    def actuacion_combobox_changed(self, row, col, index):
        combo_box = self.table.cellWidget(row, col)
        selected_value = combo_box.currentText()
        self.actu_sec_combo_box[(row, col)] = selected_value

    def delete_row(self):
        selected_row = self.table.currentRow()
        if selected_row >= 0:
            self.table.removeRow(selected_row)
        else:
            QMessageBox.information(self, "Información", "Selecciona una fila para eliminar.")

    def save_data(self):
        if self.table.rowCount() == 0:
            QMessageBox.warning(self, "Advertencia", "No se ha agregado ninguna fila.")
            return
     
        db_connection = mysql.connector.connect(
            host='causas.mysql.database.azure.com', 
            user='admin_carlos',
            password='F14tomcat',
            database='matias1'
        )

        try:
            cursor = db_connection.cursor()
            fecha_actual = datetime.now()
            self.fecha_hora_formateada = fecha_actual.strftime("%Y-%m-%d %H:%M:%S")

            for row_idx in range(self.table.rowCount()):
                self.numjui = self.table.item(row_idx, 0).text()
                nombTribunal = self.selecciones_combo_box.get((row_idx, 1), '')
                self.demandante = self.table.item(row_idx, 2).text()
                self.demandado = self.table.item(row_idx, 3).text()
                self.repre = self.table.item(row_idx, 4).text()
                self.mandante = self.table.item(row_idx, 5).text()
                self.domicilio = self.table.item(row_idx, 6).text()
                self.comuna = self.table.item(row_idx, 7).text()
                self.encargo = self.table.item(row_idx, 8).text()
                self.soli = self.table.item(row_idx, 9).text()
                self.arancel = self.table.item(row_idx, 10).text()
                actu = self.actu_sec_combo_box.get((row_idx, 11), '')

                try:
                    arancel = float(self.arancel)
                except ValueError:
                    arancel = 0  # Valor predeterminado si la conversión falla

                if any([not cell for cell in [self.numjui, nombTribunal, self.demandante, self.demandado, self.repre,
                                              self.mandante, self.domicilio, self.comuna, self.encargo,
                                              self.soli, self.arancel, actu]]):
                    QMessageBox.critical(self, "Error", "No se permiten celdas vacías en la fila {}".format(row_idx + 1))
                    db_connection.rollback()
                    return
                insert_query = "INSERT INTO demanda (numjui, nombTribunal, demandante, demandado, repre, mandante, domicilio, comuna, encargo, soli, arancel, actu) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                cursor.execute(insert_query, (self.numjui, nombTribunal, self.demandante, self.demandado, self.repre,
                                              self.mandante, self.domicilio, self.comuna, self.encargo, self.soli, arancel, actu))
                
            db_connection.commit()
            db_connection.close()
            self.clear_table()
            self.nombTribunal = nombTribunal
            QMessageBox.information(self, "Éxito", "Datos guardados correctamente")
            logging.info(f'Insercion de causa {self.numjui}-{self.encargo}')

            respuesta = QMessageBox.question(self, 'Confirmación', '¿Desea hacer seguimiento de la causa?', QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
            if respuesta == QMessageBox.StandardButton.Yes:
                self.abrir_dashboard_actuaciones(self.nombTribunal)
        except Exception as e:
            print(e)
            QMessageBox.critical(self, "Error", "Error al guardar los datos")
            db_connection.rollback()

    def abrir_dashboard_actuaciones(self, nombTribunal):
        self.dashact = Dashboard_actuacionesApp(self.numjui, nombTribunal, self.fecha_hora_formateada)
        self.dashact.show()
    
    def ajustar_tamanio(self):
        self.table.resizeColumnsToContents()
        total_width = sum(self.table.columnWidth(col) for col in range(self.table.columnCount()))
        min_width = max(self.width(), total_width)
        self.setMinimumWidth(min_width + 110)
        self.resize(total_width, self.height())
        self.adjustSize()

    def clear_table(self):
        self.table.setRowCount(0)

# Función principal
def main():
    app = QApplication(sys.argv)
    window = MiApp()
    window.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
