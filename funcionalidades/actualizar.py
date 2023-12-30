from PyQt6.QtCore import Qt, QTimer, QThread, pyqtSignal
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QPushButton, QLabel, QWidget
import sys
import time

class DatabaseWorker(QThread):
    data_updated = pyqtSignal()

    def run(self):
        while True:
            # Verificar la base de datos para nuevos datos aquí
            # Emite la señal si hay nuevos datos
            self.data_updated.emit()
            time.sleep(5)  # Espera de 5 segundos (ajusta según sea necesario)

class MyApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Datos de la Base de Datos")
        self.setGeometry(100, 100, 400, 200)

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()

        self.label = QLabel("No hay datos nuevos", self)
        self.layout.addWidget(self.label)

        self.update_button = QPushButton("Actualizar", self)
        self.update_button.clicked.connect(self.update_data_manually)
        self.layout.addWidget(self.update_button)

        self.central_widget.setLayout(self.layout)

        self.database_worker = DatabaseWorker()
        self.database_worker.data_updated.connect(self.update_data)
        self.database_worker.start()

    def update_data(self):
        # Esta función se llama cuando hay nuevos datos en la base de datos
        # Actualiza la interfaz de usuario según sea necesario
        self.label.setText("¡Hay nuevos datos!")

    def update_data_manually(self):
        # Esta función se llama cuando se hace clic en el botón de actualización manual
        # Realiza alguna acción manual y, si es necesario, emite la señal para actualizar
        # la interfaz de usuario
        print("Actualización manual realizada")
        self.database_worker.data_updated.emit()

def main():
    app = QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()

