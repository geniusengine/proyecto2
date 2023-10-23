import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QTableWidget, QTableWidgetItem, QFileDialog, QMessageBox
import pandas as pd
import mysql.connector
from PyQt6.QtGui import QColor


class DashboardApp(QMainWindow):
    def __init__(self):
        super().__init()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Dashboard App')
        self.setGeometry(100, 100, 800, 600)

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()

        self.btn_ingresar = QPushButton('Ingresar', self)
        self.btn_ingresar.clicked.connect(self.ingresar_clicked)

        self.btn_mostrar = QPushButton('Mostrar', self)
        self.btn_mostrar.clicked.connect(self.mostrar_clicked)

        self.table = QTableWidget()

        self.layout.addWidget(self.btn_ingresar)
        self.layout.addWidget(self.btn_mostrar)
        self.layout.addWidget(self.table)

        self.central_widget.setLayout(self.layout)

        # Lista ficticia de elementos
        self.elementos = [
            {"nombre": "Elemento 1", "notificada": True, "estampada": True},
            {"nombre": "Elemento 2", "notificada": True, "estampada": False},
            {"nombre": "Elemento 3", "notificada": False, "estampada": False}
        ]

    def ingresar_clicked(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Abrir archivo Excel", "", "Archivos Excel (*.xlsx)")

        if file_path:
            try:
                loaded_data = pd.read_excel(file_path)
                if not loaded_data.empty:
                    self.populate_table_with_filtered_data(loaded_data)
                
                # Conexión a la base de datos MySQL
                    conn = mysql.connector.connect(
                        host='tu_host',
                        user='tu_usuario',
                        password='tu_contraseña',
                        database='tu_base_de_datos'
                    )

                    cursor = conn.cursor()

                    for row_index in range(loaded_data.shape[0]):
                        data = [str(loaded_data.iat[row_index, col]) for col in range(loaded_data.shape[1])]

                        query = "INSERT INTO tu_tabla (campo1, campo2, campo3, campo4, campo5, campo6, campo7) VALUES (%s, %s, %s, %s, %s, %s, %s)"
                        cursor.execute(query, data)

                    conn.commit()
                    conn.close()
                
                    QMessageBox.information(self, "Éxito", "Los datos se han ingresado en la base de datos.")
                else:
                    QMessageBox.warning(self, "Aviso", "El archivo Excel está vacío.")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Error al cargar y guardar los datos: {str(e)}")

    def mostrar_clicked(self):
        self.table.setRowCount(0)

        for row_index, elemento in enumerate(self.elementos):
            self.table.insertRow(row_index)
            for col_index, (key, value) in enumerate(elemento.items()):
                item = QTableWidgetItem(str(value))

                # Definir colores según el estado de notificación y estampado
                if key == "notificada" and value:
                    item.setBackground(QColor(0, 255, 0))  # Verde
                elif key == "notificada" and not value:
                    item.setBackground(QColor(255, 0, 0))  # Rojo
                elif key == "estampada" and value:
                    item.setBackground(QColor(0, 0, 255))  # Azul
                elif key == "estampada" and not value:
                    item.setBackground(QColor(255, 255, 255))  # Blanco

                self.table.setItem(row_index, col_index, item)

def main():
    app = QApplication(sys.argv)
    window = DashboardApp()
    window.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
