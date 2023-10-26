"""
 _______       _            _     _          ______        _                 _ 
(_______)     (_)       _  (_)   | |        (____  \      (_)               | |
 _______  ____ _  ___ _| |_ _  __| |_____    ____)  ) ____ _ _____ ____   __| |
|  ___  |/ ___) |/___|_   _) |/ _  | ___ |  |  __  ( / ___) (____ |  _ \ / _  |
| |   | | |   | |___ | | |_| ( (_| | ____|  | |__)  ) |   | / ___ | | | ( (_| |
|_|   |_|_|   |_(___/   \__)_|\____|_____)  |______/|_|   |_\_____|_| |_|\____|
    
Auteur: danie(danie.pro@gmail.com) 
buscado.py(Ɔ) 2023
Description : Saisissez la description puis « Tab »
Créé le :  mercredi 25 octobre 2023 à 20:46:11 
Dernière modification : mercredi 25 octobre 2023 à 22:25:35
"""

import sys
import mysql.connector
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QLineEdit, QVBoxLayout, QHBoxLayout, QWidget, QCheckBox, QListWidget, QListWidgetItem

class BuscadorDatosCausaApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Buscador de Datos de Causa")
        self.setGeometry(100, 100, 600, 400)

        self.initUI()

    def initUI(self):
        main_layout = QVBoxLayout()

        # Parte superior (en una sola fila)
        search_layout = QHBoxLayout()

        self.check_juicio = QCheckBox("Buscar por Número de Juicio")
        self.juicio_label = QLabel("Número de Juicio:")
        self.juicio_input = QLineEdit(self)
        search_layout.addWidget(self.check_juicio)
        search_layout.addWidget(self.juicio_label)
        search_layout.addWidget(self.juicio_input)

        self.check_tribunal = QCheckBox("Buscar por Tribunal")
        self.tribunal_label = QLabel("Tribunal:")
        self.tribunal_input = QLineEdit(self)
        search_layout.addWidget(self.check_tribunal)
        search_layout.addWidget(self.tribunal_label)
        search_layout.addWidget(self.tribunal_input)

        self.button_search = QPushButton("Buscar", self)
        self.button_search.clicked.connect(self.search_data)
        search_layout.addWidget(self.button_search)

        main_layout.addLayout(search_layout)

        # Parte inferior (resultados con casillas de verificación y botones)
        self.result_list = QListWidget(self)
        main_layout.addWidget(self.result_list)

        self.result_checkboxes = []

        self.buttons_layout = QHBoxLayout()
        self.button_select = QPushButton("Seleccionar", self)
        self.button_select.clicked.connect(self.select_results)
        self.buttons_layout.addWidget(self.button_select)

        self.button_clear = QPushButton("Limpiar", self)
        self.button_clear.clicked.connect(self.clear_results)
        self.buttons_layout.addWidget(self.button_clear)

        main_layout.addLayout(self.buttons_layout)

        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

    def search_data(self):
        search_by_juicio = self.check_juicio.isChecked()
        search_by_tribunal = self.check_tribunal.isChecked()
        numero_juicio = self.juicio_input.text()
        tribunal = self.tribunal_input.text()

        if not search_by_juicio and not search_by_tribunal:
            self.result_list.clear()
            item = QListWidgetItem("Por favor, seleccione al menos un criterio de búsqueda.")
            self.result_list.addItem(item)
            return

        try:
            connection = mysql.connector.connect(
                host='localhost',  # Cambia esto a la dirección de tu servidor MySQL
                user='root',  # Cambia esto a tu nombre de usuario de MySQL
                password='',  # Cambia esto a tu contraseña de MySQL
                database='mi_causa'  # Cambia esto al nombre de tu base de datos
            )

            cursor = connection.cursor()

            if search_by_juicio and not search_by_tribunal:
                query = "SELECT NumeroJuicio, tribunal FROM datoscausas WHERE NumeroJuicio = %s"
                cursor.execute(query, (numero_juicio,))
            elif not search_by_juicio and search_by_tribunal:
                query = "SELECT NumeroJuicio, tribunal FROM datoscausas WHERE tribunal = %s"
                cursor.execute(query, (tribunal,))
            else:
                query = "SELECT NumeroJuicio, tribunal FROM datoscausas WHERE NumeroJuicio = %s AND tribunal = %s"
                cursor.execute(query, (numero_juicio, tribunal))

            data = cursor.fetchall()
            connection.close()

            self.result_list.clear()
            self.result_checkboxes.clear()

            if data:
                for row in data:
                    result = f"Numero de Juicio: {row[0]}, Tribunal: {row[1]}"
                    item = QListWidgetItem(result)
                    checkbox = QCheckBox()
                    self.result_list.addItem(item)
                    self.result_list.setItemWidget(item, checkbox)
                    self.result_checkboxes.append(checkbox)
            else:
                item = QListWidgetItem("No se encontraron datos para la búsqueda especificada.")
                self.result_list.addItem(item)

        except mysql.connector.Error as err:
            self.result_list.clear()
            item = QListWidgetItem(f"Error: {err}")
            self.result_list.addItem(item)

    def select_results(self):
        selected_results = [self.result_list.item(i) for i, checkbox in enumerate(self.result_checkboxes) if checkbox.isChecked()]
        if selected_results:
            selected_data = [item.text() for item in selected_results]
            selected_data = "\n".join(selected_data)
            self.result_list.clear()
            item = QListWidgetItem(selected_data)
            self.result_list.addItem(item)
        else:
            self.result_list.clear()
            item = QListWidgetItem("Ningún resultado seleccionado")

    def clear_results(self):
        self.result_list.clear()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = BuscadorDatosCausaApp()
    window.show()
    sys.exit(app.exec())
