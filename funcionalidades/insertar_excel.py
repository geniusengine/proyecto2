"""
 _______       _            _     _          ______        _                 _ 
(_______)     (_)       _  (_)   | |        (____  \      (_)               | |
 _______  ____ _  ___ _| |_ _  __| |_____    ____)  ) ____ _ _____ ____   __| |
|  ___  |/ ___) |/___|_   _) |/ _  | ___ |  |  __  ( / ___) (____ |  _ \ / _  |
| |   | | |   | |___ | | |_| ( (_| | ____|  | |__)  ) |   | / ___ | | | ( (_| |
|_|   |_|_|   |_(___/   \__)_|\____|_____)  |______/|_|   |_\_____|_| |_|\____|
    
Auteur: daniel(mitchel.dmch@gmail.com) 
insertar.py(Ɔ) 2023
Description : Saisissez la description puis « Tab »
Créé le :  samedi 4 novembre 2023 à 16:15:10 
Dernière modification : lundi 22 janvier 2024 à 22:47:07
"""

import sys
import pymssql
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QFileDialog, QTableWidget, QTableWidgetItem, QLineEdit, QVBoxLayout, QWidget, QMessageBox
import openpyxl
from PyQt6.QtGui import QIcon
import logging

# Configurar el sistema de registro
logging.basicConfig(filename='registro.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class ExcelToDatabaseApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setWindowTitle("Insertar Excel")
        self.setWindowIcon(QIcon("static/icons/icono-ventana.png"))
        self.setGeometry(100, 100, 800, 400)

        self.upload_button = QPushButton("Cargar Excel", self)
        self.upload_button.clicked.connect(self.uploadExcel)

        self.save_button = QPushButton("Guardar", self)
        self.save_button.clicked.connect(self.saveData)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        layout = QVBoxLayout(self.central_widget)

        self.data_table = QTableWidget(self)
        self.data_table.setColumnCount(12)  # 5 para los datos Excel, 1 para "arancel", 1 para "tribunal"
        self.data_table.setHorizontalHeaderLabels([ 'Rol', 'Tribunal', 'Nombre demandante', 'Apellido demandante', 'Nombre demandando', 'Representante', 'Nombre mandante', 'Domicilio', 'Comuna', 'Encargo', 'Solicitud', 'Arancel'])
        layout.addWidget(self.data_table)
        

        layout.addWidget(self.upload_button)
        layout.addWidget(self.save_button)
        self.ajustar_tamanio()
        self.excel_data = None
    # Reemplaza 'self.table' con 'self.data_table'
    def ajustar_tamanio(self):
        self.data_table.resizeColumnsToContents()
        total_width = sum(self.data_table.columnWidth(col) for col in range(self.data_table.columnCount()))
        min_width = max(self.width(), total_width)
        self.setMinimumWidth(min_width + 0)
        self.adjustSize()


    def uploadExcel(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Selecciona un archivo Excel", "", "Excel Files (*.xlsx);;All Files (*)")

        if file_name:
            # Leer datos del archivo Excel usando openpyxl
            workbook = openpyxl.load_workbook(file_name)
            sheet = workbook.active
            self.excel_data = [row for row in sheet.iter_rows(values_only=True)]

            self.data_table.setRowCount(len(self.excel_data))
            for row_idx, row in enumerate(self.excel_data):
                for col_idx, cell_value in enumerate(row):
                    item = QTableWidgetItem(str(cell_value))
                    self.data_table.setItem(row_idx, col_idx, item)
                    if col_idx == 13:  # Columna "Arancel"
                        arancel_input = QLineEdit()
                        self.data_table.setCellWidget(row_idx, 13, arancel_input)
                    

    def saveData(self):
        if self.excel_data is None:
            return  # No hay datos de Excel cargados

        # Conectar a la base de datos SQL Server
        db_connection = pymssql.connect(
                server='vps-3697915-x.dattaweb.com',
                user='daniel',
                password='LOLxdsas--',
                database='micau5a'
        )
        try:
            cursor = db_connection.cursor()

            for row_idx in range(self.data_table.rowCount()):
                numjui = self.data_table.item(row_idx, 1).text()
                nombTribunal = self.data_table.item(row_idx, 2).text()
                nombdemandante = self.data_table.item(row_idx, 3).text()
                apellidemandante = self.data_table.item(row_idx, 4).text()
                demandado = self.data_table.item(row_idx, 5).text()
                repre = self.data_table.item(row_idx, 6).text()
                mandante = self.data_table.item(row_idx, 7).text()
                domicilio = self.data_table.item(row_idx, 8).text()
                comuna = self.data_table.item(row_idx, 9).text()
                encargo = self.data_table.item(row_idx, 10).text()
                soli = self.data_table.item(row_idx, 11).text()

                arancel_text = self.data_table.item(row_idx, 12).text()
                print(arancel_text)
                try:
                        arancel = (arancel_text)
                except ValueError:
                        arancel = 0  # Valor predeterminado si la conversión falla
                
            # Insertar datos de la demanda en la tabla "demanda"
            insert_query = "INSERT INTO demanda (numjui,nombTribunal,nombdemandante,apellidemandante,demandado,repre,mandante,domicilio,comuna,encargo,soli,arancel) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            cursor.execute(insert_query, (numjui,nombTribunal,nombdemandante,apellidemandante,demandado,repre,mandante,domicilio,comuna,encargo,soli,arancel))
            db_connection.commit()
            db_connection.close()
        
             # Mensaje de éxito y limpiar la ventana
            QMessageBox.information(self, "Éxito", "Datos guardados correctamente.")
            self.data_table.clearContents()  # Limpiar datos de la tabla
            self.data_table.setRowCount(0)  # Restablecer el número de filas
        except Exception as e:
            print(e)
            QMessageBox.critical(self, "Error", "Error al guardar los datos")
            db_connection.rollback()
        # Proporciona retroalimentación al usuario

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ExcelToDatabaseApp()
    window.show()
    sys.exit(app.exec())
