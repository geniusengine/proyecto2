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
Dernière modification : lundi 4 décembre 2023 à 19:30:56
"""
import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QTableWidget, QTableWidgetItem, QPushButton, QWidget, QMessageBox,QHBoxLayout
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QLineEdit  # Agregado para importar QLineEdit

import pymssql

class MiApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Ingreso de Datos")
        self.setGeometry(100, 100, 800, 400)

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        layout = QHBoxLayout()
        layout_vertical = QVBoxLayout()

        self.table = QTableWidget()
        self.table.setColumnCount(14)
        self.table.setHorizontalHeaderLabels(['Rol', 'Tribunal', 'Nombre demandante', 'Apellido demandante', 'Nombre demandando', 'Apellido demandando', 'Nombre mandante', 'Apellido mandante', 'Representante', 'Domicilio', 'Comuna', 'Solicitud', 'Encargo', 'Arancel'])
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
    def add_row(self):
        self.table.insertRow(self.table.rowCount())
        
    def delete_row(self):
        selected_row = self.table.currentRow()
        if selected_row >= 0:
            self.table.removeRow(selected_row)
        else:
            QMessageBox.information(self, "Información", "Selecciona una fila para eliminar.")


    def save_data(self):
        db_connection = pymssql.connect(
            server='vps-3697915-x.dattaweb.com',
            user='daniel',
            password='LOLxdsas--',
            database='micau5a')
        try:
            cursor = db_connection.cursor()

            for row_idx in range(self.table.rowCount()):
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

                if all([numjui,nombTribunal,nombdemandante,apellidemandante,nombdemandado,apellidemandado,nombmandante,apellimandante,repre,domicilio,comuna,solicitante,encargo,arancel]):
                    insert_query = "INSERT INTO demanda (numjui,nombTribunal,nombdemandante,apellidemandante,nombdemandado,apellidemandado,nombmandante,apellimandante,repre,domicilio,comuna,soli,encargo,arancel) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                    cursor.execute(insert_query, (numjui,nombTribunal,nombdemandante,apellidemandante,nombdemandado,apellidemandado,nombmandante,apellimandante,repre,domicilio,comuna,solicitante,encargo,arancel))
                else:
                    QMessageBox.critical(self, "Error", "No se permiten celdas vacías en la fila {}".format(row_idx + 1))
                    db_connection.rollback()
                    break

            db_connection.commit()
            db_connection.close()

            self.clear_table()
            QMessageBox.information(self, "Éxito", "Datos guardados correctamente")
        except Exception as e:
            print(e)
            QMessageBox.critical(self, "Error", "Error al guardar los datos")
            db_connection.rollback()

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

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MiApp()
    window.show()
    sys.exit(app.exec())
