import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QTableWidget, QTableWidgetItem, QFileDialog, QMessageBox
import pandas as pd
import mysql.connector
import estampar
import pymssql
from coneccion2 import DatabaseApp
from PyQt6.QtGui import QColor
from verCausa import VerCausaApp


class DashboardApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Dashboard App')
        self.setGeometry(100, 100, 1050, 600)

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()#crea un layout vertical para los botones y la tabla

        self.btn_ingresar = QPushButton('Ingresar', self)
        self.btn_ingresar.clicked.connect(self.ingresar_clicked)

        self.btn_mostrar = QPushButton('Mostrar', self)
        self.btn_mostrar.clicked.connect(self.mostrar_clicked)

        self.table = QTableWidget()#crea una tabla vacia para mostrar los datos

        self.layout.addWidget(self.btn_ingresar)
        self.layout.addWidget(self.btn_mostrar)
        self.layout.addWidget(self.table)

        self.central_widget.setLayout(self.layout)

    def estampar_clicked(self):
        # Manejar la lógica cuando se hace clic en el botón de estampado
        button = self.sender()  # Obtener el botón que emitió la señal
        index = self.table.indexAt(button.pos())  # Obtener la posición del botón en la tabla
        row, col = index.row(), index.column()
        #llama a la ventana estampado
        self.estampado_app = estampado.EstampadoApp()
        self.estampado_app.show()

    def verCausa_clicked(self):
        # Manejar la lógica cuando se hace clic en el botón de VerCausa
        button = self.sender()  # Obtener el botón que emitió la señal
        index = self.table.indexAt(button.pos())  # Obtener la posición del botón en la tabla
        row, col = index.row(), index.column()
        #llama a la ventana verCausa
        self.vercausa_app = VerCausaApp()
        self.vercausa_app.show()   

    def ingresar_clicked(self):
        # Conectar a la base de datos MySQL
        conn = pymssql.connect(
                server='vps-3697915-x.dattaweb.com',
                user='daniel',
                password='LOLxdsas--',
                database='micau5a'
        )
        
        # Crear un cursor
        cursor = conn.cursor()

        # Ejecutar una consulta SELECT

        query = "SELECT fechaNotificacion,rutDemandado,rutMandante,rolCausa,nombTribunal,notificacion FROM notificacion"
        cursor.execute(query)

        # Obtener todos los resultados
        resultados = cursor.fetchall()

        # Lista que contendrá los diccionarios
        self.elementos = []


        # Iterar sobre los resultados y agregarlos al diccionario

        for fila in resultados:
            # Crear un diccionario para cada fila
            elemento = {
                "Fecha": fila[0],
                "Rut Demandado": fila[1],
                "Rut Mandante": fila[2],
                "Rol Causa": fila[3],
                "Tribunal": fila[4],
                "Notificada": fila[5],
                "Estampada": True,#Se necesita cambiar esto segun de donde3 vengan estos datos de la bd
                "VerCausa": True,#Se necesita cambiar esto segun de donde3 vengan estos datos de la bd
            }
            self.elementos.append(elemento)

        # Mostrar los diccionarios
        for elemento in self.elementos:
            print(elemento)

        # Cerrar el cursor y la conexión
        cursor.close()
        conn.close()
    def mostrar_clicked(self):
        self.table.setColumnCount(8)  # Número de columnas
        self.table.setHorizontalHeaderLabels(['Fecha','Rut demandado','Rut mandante','Rol Causa','Tribunal','notificada','Estampada','Ver Causa'])  # Etiquetas de las columnas
        
        #
        for row_index, elemento in enumerate(self.elementos):#row_index es el indice de la fila y segun los elementos que haya en la lista elementos se crean las filas
            self.table.insertRow(row_index)#inserta al final de la tabla una fila
            notificada = elemento["Notificada"]#obtiene el valor de la llave notificada
            estampada = elemento["Estampada"]#obtiene el valor de la llave estampada
            for col_index, (key, value) in enumerate(elemento.items()):#col_index es el indice de la columna
                item = QTableWidgetItem(str(value))#crea un item con el valor de la celda
                #establecer un boton en la celda de estampado
                if key == "Estampada":
                    button = QPushButton("Estampar", self)
                    button.clicked.connect(self.estampar_clicked)
                    self.table.setCellWidget(row_index, col_index, button)
                #establecer un boton en la celda de ver causa
                if key == "VerCausa":
                    button = QPushButton("Ver Causa", self)
                    button.clicked.connect(self.verCausa_clicked)
                    self.table.setCellWidget(row_index, col_index, button)  
#------------------------------------------------------------------------------------
                if estampada == True and notificada == True:
                    item.setBackground(QColor(0, 255, 0))#establece el color de fondo de la celda en verde
                    self.table.setVerticalHeaderLabels(['Verde'])
                if  estampada == True and notificada == False:
                    item.setBackground(QColor(255, 255, 0))#establece el color de fondo de la celda en amarillo
                    self.table.setVerticalHeaderLabels(['Amarillo'])
                if estampada == False and notificada == True:
                    item.setBackground(QColor(0, 0, 255))#establece el color de fondo de la celda en azul
                    self.table.setVerticalHeaderLabels(['Azul'])
                if estampada == False and notificada == False:
                    item.setBackground(QColor(255, 0, 0))#establece el color de fondo de la celda en rojo
                    self.table.setVerticalHeaderLabels(['Rojo'])
                 
                self.table.setItem(row_index, col_index, item)#establece el item en la celda correspondiente 



        

def main():
    app = QApplication(sys.argv)
    window = DashboardApp()
    window.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
