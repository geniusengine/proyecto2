import pymssql
import subprocess  # Importa el módulo subprocess
import sys
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

        self.check_numjui = QCheckBox("rol o tribunal")
        self.numjui_label = QLabel("rol o tribunal:")
        self.numjui_input = QLineEdit(self)
        search_layout.addWidget(self.check_numjui)
        search_layout.addWidget(self.numjui_label)
        search_layout.addWidget(self.numjui_input)

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
        search_by_numjui = self.check_numjui.isChecked()
        numjui = self.numjui_input.text()

        if not search_by_numjui:
            self.result_list.clear()
            item = QListWidgetItem("Por favor, seleccione al menos un criterio de búsqueda.")
            self.result_list.addItem(item)
            return

        try:
            connection = pymssql.connect(
                server='vps-3697915-x.dattaweb.com',
                user='daniel',
                password='LOLxdsas--',
                database='micau5a'
            )

            cursor = connection.cursor()

            query = """
            SELECT fechaNotificacion, numjui, nombTribunal, nombdemandante, apellidemandante, nombdemandado, apellidemandado, nombmandante, apellimandante, repre, domicilio, comuna, soli, encargo, arancel, estadoNoti, estadoCausa
            FROM notificacion
            WHERE numjui = %s OR nombtribunal = %s
            """
            cursor.execute(query, (numjui, numjui))

            data = cursor.fetchall()
            connection.close()

            self.result_list.clear()
            self.result_checkboxes.clear()

            if data:
                for row in data:
                    result = f"Rol: {row[0]}, Tribunal: {row[1]}"
                    item = QListWidgetItem(result)
                    checkbox = QCheckBox()
                    self.result_list.addItem(item)
                    self.result_list.setItemWidget(item, checkbox)
                    self.result_checkboxes.append(checkbox)
            else:
                item = QListWidgetItem("No se encontraron datos para la búsqueda especificada.")
                self.result_list.addItem(item)

        except pymssql.Error as err:
            self.result_list.clear()
            item = QListWidgetItem(f"Error: {err}")
            self.result_list.addItem(item)

    def select_results(self):
        selected_results = [self.result_list.item(i) for i, checkbox in enumerate(self.result_checkboxes) if checkbox.isChecked()]
        if selected_results:
            selected_data = [item.text() for item in selected_results]
            selected_data = "\n".join(selected_data)
            item = QListWidgetItem(selected_data)
            self.result_list.addItem(item)
        else:
            self.result_list.clear()
            item = QListWidgetItem("Ningún resultado seleccionado")


        try:
            connection = pymssql.connect(
                server='vps-3697915-x.dattaweb.com',
                user='daniel',
                password='LOLxdsas--',
                database='micau5a'
            )

            cursor = connection.cursor()

            selected_data = []
            for result_item in selected_results:
                numjui = result_item.text().split(',')[0].split(':')[-1].strip()
                nombtribunal = result_item.text().split(',')[1].split(':')[-1].strip()
                
                query = """
            SELECT fechaNotificacion, numjui, nombTribunal, nombdemandante, apellidemandante, nombdemandado, apellidemandado, nombmandante, apellimandante, repre, domicilio, comuna, soli, encargo, arancel, estadoNoti, estadoCausa
            FROM notificacion
            WHERE numjui = %s OR nombtribunal = %s
            """
                cursor.execute(query, (numjui, nombtribunal))
                data = cursor.fetchall()
                selected_data.extend(data)

            connection.close()

            self.result_list.clear()
            if selected_data:
                for row in selected_data:
                    result = f"Rol: {row[0]}, Tribunal: {row[1]}, 'Nombre demandante'{row[2]}, 'Apellido demandante'{row[3]}, 'Nombre demandando'{row[4]},{row[5]},'Apellido demandando'{row[6]},'Nombre mandante'{row[7]},Apellido mandante'{row[8]},'Representante'{row[10]},'Domicilio'{row[11]},'Comuna'{row[12]},'Solicitante'{row[13]},'Encargo'{row[14]},'Arancel'{row[15]},'Notificada'{row[16]},'E.C'{row[15]},'Notificar'{row[17]},'Estampar'{row[18]},'Ver Causa' {row[19]}"
                    item = QListWidgetItem(result)
                    self.result_list.addItem(item)

                # Llamar al script externo
                subprocess.run(['python', 'estampado_app.py'])
            else:
                item = QListWidgetItem("No se encontraron datos para la búsqueda especificada.")
                self.result_list.addItem(item)

        except pymssql.Error as err:
            self.result_list.clear()
            item = QListWidgetItem(f"Error: {err}")
            self.result_list.addItem(item)

    def clear_results(self):
        self.result_list.clear()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = BuscadorDatosCausaApp()
    window.show()
    sys.exit(app.exec())
