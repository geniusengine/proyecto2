import os
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget
from docx import Document
from docx2pdf import convert
from datetime import datetime
import tkinter as tk
from tkinter import filedialog
class EstampadoActuaciones(QMainWindow):
    def __init__(self,numjui, nombTribunal,fecha,parent=None):
        super().__init__(parent)

        self.setWindowTitle('Ventana con Botones')
        self.setGeometry(100, 100, 400, 200)

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        # Layout vertical para organizar los botones
        layout_vertical = QVBoxLayout(self.central_widget)

        # Crear botones
        boton1 = QPushButton('Negativa 52', self)
        boton1.clicked.connect(self.estampar_1)

        boton2 = QPushButton('Negativa Personal', self)
        boton2.clicked.connect(self.estampar_2)

        boton3 = QPushButton('Positivo', self)
        boton3.clicked.connect(self.estampar_3)

        boton4 = QPushButton('Busqueda y Notificacion', self)
        boton4.clicked.connect(self.estampar_4)

        boton5 = QPushButton('Notificacion Personal', self)
        boton5.clicked.connect(self.estampar_5)




    # Botones enlazados con sus opciones correspindientes    
    def estampar_1(self):
        self.negativa52()

    def estampar_2(self):
        self.negativaP()

    def estampar_3(self):
        self.positivaP()

    def estampar_4(self):
        self.busquedaN()

    def estampar_5(self):
        self.notificacionP()



def main():
    app = QApplication([])
    ventana = EstampadoActuaciones()
    ventana.show()
    app.exec()

if __name__ == '__main__':
    main()
