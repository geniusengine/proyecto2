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
Dernière modification : vendredi 29 décembre 2023 à 23:50:27
"""

import sys
import pymssql
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QFileDialog, QTableWidget, QTableWidgetItem, QLineEdit, QVBoxLayout, QWidget, QMessageBox
import openpyxl

class ExcelToDatabaseApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setWindowTitle("Excel to Database App")
        self.setGeometry(100, 100, 800, 400)

        self.upload_button = QPushButton("Cargar Excel", self)
        self.upload_button.clicked.connect(self.uploadExcel)

        self.save_button = QPushButton("Guardar", self)
        self.save_button.clicked.connect(self.saveData)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        layout = QVBoxLayout(self.central_widget)

        self.data_table = QTableWidget(self)
        self.data_table.setColumnCount(14)  # 5 para los datos Excel, 1 para "arancel", 1 para "tribunal"
        self.data_table.setHorizontalHeaderLabels(['Rol', 'Tribunal', 'Nombre demandante', 'Apellido demandante', 'Nombre demandando', 'Apellido demandando', 'Nombre mandante', 'Apellido mandante', 'Representante', 'Domicilio', 'Comuna', 'Solicitud', 'Encargo', 'Arancel'])
        layout.addWidget(self.data_table)
        

        layout.addWidget(self.upload_button)
        layout.addWidget(self.save_button)

        self.excel_data = None

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
                numjui= self.table.item(row_idx, 0).text()
                nombTribunal= self.table.item(row_idx, 1).text()
                nombdemandante= self.table.item(row_idx, 2).text()
                apellidemandante= self.table.item(row_idx, 3).text()
                nombdemandado= self.table.item(row_idx, 4).text()
                apellidemandado= self.table.item(row_idx, 5).text()
                nombmandante= self.table.item(row_idx, 6).text()
                apellimandante= self.table.item(row_idx, 7).text()
                repre= self.table.item(row_idx, 8).text()
                domicilio= self.table.item(row_idx, 9).text()
                comuna= self.table.item(row_idx, 10).text()
                solicitante= self.table.item(row_idx, 11).text()
                encargo= self.table.item(row_idx, 12).text()
                arancel= self.table.item(row_idx, 13).text()

                arancel_text = self.table.item(row_idx, 13).text()
                print(arancel_text)
                try:
                        arancel = (arancel_text)
                except ValueError:
                        arancel = 0  # Valor predeterminado si la conversión falla
                

        

            # Insertar datos de la demanda en la tabla "demanda"
            insert_query = "INSERT INTO demanda (numjui,nombTribunal,nombdemandante,apellidemandante,nombdemandado,apellidemandado,nombmandante,apellimandante,repre,domicilio,comuna,soli,encargo,arancel) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            cursor.execute(insert_query, (numjui,nombTribunal,nombdemandante,apellidemandante,nombdemandado,apellidemandado,nombmandante,apellimandante,repre,domicilio,comuna,solicitante,encargo,arancel))
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
