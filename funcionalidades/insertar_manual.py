"""
 _______       _            _     _          ______        _                 _ 
(_______)     (_)       _  (_)   | |        (____  \      (_)               | |
 _______  ____ _  ___ _| |_ _  __| |_____    ____)  ) ____ _ _____ ____   __| |
|  ___  |/ ___) |/___|_   _) |/ _  | ___ |  |  __  ( / ___) (____ |  _ \ / _  |
| |   | | |   | |___ | | |_| ( (_| | ____|  | |__)  ) |   | / ___ | | | ( (_| |
|_|   |_|_|   |_(___/   \__)_|\____|_____)  |______/|_|   |_\_____|_| |_|\____|
    
Auteur: daniel(mitchel.dmch@gmail.com) 
manualapajas.py(Ɔ) 2023
Description : Saisissez la description puis « Tab »
Créé le :  samedi 4 novembre 2023 à 17:40:55 
Dernière modification : mercredi 31 janvier 2024 à 12:00:31
"""
import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QTableWidget, QTableWidgetItem, QPushButton, QWidget, QMessageBox,QHBoxLayout,QComboBox
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QLineEdit  # Agregado para importar QLineEdit
from datetime import datetime
import pymssql
from .dashboard_actuaciones import Dashboard_actuacionesApp
from .estampado_app import Estampadoxd
import logging
import pyodbc
import time


# Configurar el sistema de registro
logging.basicConfig(filename='registro.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class MiApp(QMainWindow):
    

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Ingreso de Datos")
        self.setWindowIcon(QIcon("static/icono-ventana.png"))
        self.setGeometry(100, 100, 800, 400)

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        layout = QHBoxLayout()
        layout_vertical = QVBoxLayout()
        
        self.table = QTableWidget()
        self.table.setColumnCount(10)
        self.table.setHorizontalHeaderLabels(['Rol', 'Tribunal', 'Demandante', 'Demandando', 'Representante', 'Domicilio', 'Comuna', 'Encargo', 'Resultado', 'Arancel'])
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
        if item.column() == 11:
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
                                    'Juzgado de Letras del Trabajo de La Serena',
                                    'Juzgado de Garantía La Serena',
                                    'Juzgado de Juicio Oral en lo Penal La Serena',
                                    'Juzgado de Familia La Serena',
                                    'Corte de Apelaciones de La Serena'])
        
        # Configura el nuevo QComboBox en la celda correspondiente
        item = QTableWidgetItem()
        self.table.setItem(self.table.rowCount() - 1, 1, item)
        self.table.setCellWidget(self.table.rowCount() - 1, 1, tribunal_combobox)
        
    def combo_box_changed(self, row, col, index):
    # Obtén el valor actual del combo box
        combo_box = self.table.cellWidget(row, col)
        selected_value = combo_box.currentText()  # Agrega los paréntesis para obtener el texto actual

    # Lista de tribunales
        tribunales = ['1° Juzgado de Letras La Serena',
                  '2° Juzgado de Letras La Serena',
                  '3° Juzgado de Letras La Serena',
                  'Juzgado de Letras del Trabajo de La Serena',
                  'Juzgado de Garantía La Serena',
                  'Juzgado de Juicio Oral en lo Penal La Serena',
                  'Juzgado de Familia La Serena',
                  'Corte de Apelaciones de La Serena']

    # Llena el QComboBox con los tribunales
        combo_box.clear()
        combo_box.addItems(tribunales)

    # Asigna el valor seleccionado actualmente
        combo_box.setCurrentText(selected_value)

           



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
     
                       
        db_connection = pymssql.connect(
            server='vps-3697915-x.dattaweb.com',
            user='daniel',
            password='LOLxdsas--',
            database='micau5a')

        try:
            cursor = db_connection.cursor()
            fecha_actual = datetime.now()
            self.fecha_hora_formateada = fecha_actual.strftime("%Y-%m-%d %H:%M:%S")
            print("Fecha y hora actuales:", self.fecha_hora_formateada)

            for row_idx in range(self.table.rowCount()):
                self.numjui = self.table.item(row_idx, 0).text()
                self.nombTribunal = self.table.item(row_idx, 1).text()
                self.nombdemandante = self.table.item(row_idx, 2).text()
                self.apellidemandante = self.table.item(row_idx, 3).text()
                self.demandado = self.table.item(row_idx, 4).text()
                self.repre = self.table.item(row_idx, 5).text()
                self.mandante = self.table.item(row_idx, 6).text()
                self.domicilio = self.table.item(row_idx, 7).text()
                self.comuna = self.table.item(row_idx, 8).text()
                self.encargo = self.table.item(row_idx, 9).text()
                self.soli = self.table.item(row_idx, 10).text()
                self.arancel = self.table.item(row_idx, 11).text()
                print(self.arancel)
                try:
                    arancel = float(self.arancel)
                except ValueError:
                    arancel = 0  # Valor predeterminado si la conversión falla

                if any([not cell for cell in [self.numjui,self.nombdemandante,
                                            self.apellidemandante, self.demandado, self.repre,
                                            self.mandante, self.domicilio, self.comuna, self.encargo,
                                            self.soli, self.arancel]]):
                    QMessageBox.critical(self, "Error", "No se permiten celdas vacías en la fila {}".format(row_idx + 1))
                    db_connection.rollback()
                    return
                insert_query = "INSERT INTO demanda (numjui, nombTribunal,demandante, demandado, repre, mandante, domicilio, comuna, encargo, soli, arancel) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                cursor.execute(insert_query, (self.numjui, self.nombTribunal, self.nombdemandante,
                                            self.apellidemandante, self.demandado, self.repre,
                                            self.mandante, self.domicilio, self.comuna, self.encargo,
                                            self.soli, arancel))
            db_connection.commit()
            db_connection.close()
            self.clear_table()
            QMessageBox.information(self, "Éxito", "Datos guardados correctamente")

            logging.info(f'Insercion de causa {self.numjui}-{self.encargo}')

            respuesta = QMessageBox.question(self, 'Confirmación', '¿Desea hacer seguimiento de la causa?',QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
            if respuesta == QMessageBox.StandardButton.Yes:
                self.abrir_dashboard_actuaciones()
            else:
                pass
        except Exception as e:
            print(e)
            QMessageBox.critical(self, "Error", "Error al guardar los datos")
            db_connection.rollback()
            # Emitir la señal cuando se guardan los datos
            self.datos_guardados_signal.emit()

    def abrir_dashboard_actuaciones(self):
        # Puedes implementar el código para abrir Dashboard_actuacionesApp y enviar datos aquí
        # Por ahora, simplemente imprimimos un mensaje
        print("Abriendo Dashboard_actuacionesApp y enviando datos...")

        # Ejemplo: Crear y mostrar Dashboard_actuacionesApp
        self.dashact = Dashboard_actuacionesApp(self.numjui,self.nombTribunal,self.fecha_hora_formateada)
        self.dashact.show()
    
    def ajustar_tamanio(self):
        # Ajustar automáticamente el tamaño de las columnas
        self.table.resizeColumnsToContents()
        
        # Calcular el ancho total de las columnas
        total_width = sum(self.table.columnWidth(col) for col in range(self.table.columnCount()))
        
        # Establecer el ancho mínimo de la ventana para evitar achicarse demasiado
        min_width = max(self.width(), total_width)
        
        # Ajustar el tamaño de la ventana al tamaño máximo necesario
        self.setMinimumWidth(min_width+110)
        self.resize(total_width, self.height())  # Opcional: Ajustar también el ancho actual de la ventana
        
        # Ajustar automáticamente el tamaño de la ventana
        self.adjustSize()

    def clear_table(self):
        self.table.setRowCount(0)

# Función principal
def main():
    app = QApplication(sys.argv)
    window = Dashboard_actuacionesApp()
    

    window.show()
    sys.exit(app.exec())
    
# Ejecuta la función principal
if __name__ == '__main__':
    main()
    