"""
 _______       _            _     _          ______        _                 _ 
(_______)     (_)       _  (_)   | |        (____  \      (_)               | |
 _______  ____ _  ___ _| |_ _  __| |_____    ____)  ) ____ _ _____ ____   __| |
|  ___  |/ ___) |/___|_   _) |/ _  | ___ |  |  __  ( / ___) (____ |  _ \ / _  |
| |   | | |   | |___ | | |_| ( (_| | ____|  | |__)  ) |   | / ___ | | | ( (_| |
|_|   |_|_|   |_(___/   \__)_|\____|_____)  |______/|_|   |_\_____|_| |_|\____|
    
Auteur: danie(danie.pro@gmail.com) 
acciones.py(Ɔ) 2024
Description : Saisissez la description puis « Tab »
Créé le :  jeudi 18 janvier 2024 à 16:17:19 
Dernière modification : jeudi 18 janvier 2024 à 16:17:27
"""
import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QTextEdit
from PyQt6.QtCore import QDateTime, QTimer
import logging

class AccionesVentana(QMainWindow):
    def __init__(self, log_file_path):
        super().__init__()
        self.initUI(log_file_path)

    def initUI(self, log_file_path):
        self.setWindowTitle('Historial de Acciones')
        self.setGeometry(500, 500, 400, 300)

        self.text_edit = QTextEdit(self)
        self.text_edit.setReadOnly(True)

        with open(log_file_path, 'r') as log_file:
            acciones = log_file.readlines()

        for accion in acciones:
            self.text_edit.append(accion.strip())

        self.setCentralWidget(self.text_edit)

class DashboardApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.logger = self.iniciar_logger()

    def initUI(self):
        self.setWindowTitle('Dashboard App')
        self.setGeometry(100, 100, 400, 300)

        self.btn_accion = QPushButton('Realizar Acción', self)
        self.btn_accion.clicked.connect(self.realizar_accion)

        self.btn_ver_historial = QPushButton('Ver Historial de Acciones', self)
        self.btn_ver_historial.clicked.connect(self.mostrar_historial_acciones)

        layout = QVBoxLayout()
        layout.addWidget(self.btn_accion)
        layout.addWidget(self.btn_ver_historial)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.mostrar_hora_en_tiempo_real)
        self.timer.start(1000)  # Actualizar cada segundo

    def iniciar_logger(self):
        logger = logging.getLogger('usuario_logger')
        logger.setLevel(logging.INFO)
        handler = logging.FileHandler('acciones_usuario.log')
        formatter = logging.Formatter('%(asctime)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        return logger

    def realizar_accion(self):
        accion = 'Realizar Acción'
        self.logger.info(accion)
        print(f'Accion realizada: {accion}')

    def mostrar_hora_en_tiempo_real(self):
        hora_actual = QDateTime.currentDateTime().toString('yyyy-MM-dd HH:mm:ss')
        self.statusBar().showMessage(f'Hora: {hora_actual}')

    def mostrar_historial_acciones(self):
        acciones_ventana = AccionesVentana('acciones_usuario.log')
        acciones_ventana.show()

def main():
    app = QApplication(sys.argv)
    window = DashboardApp()
    window.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()

