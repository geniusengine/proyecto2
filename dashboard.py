import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QTableWidget, QTableWidgetItem, QFileDialog, QMessageBox
import pandas as pd
import mysql.connector
import estampar
from PyQt6.QtGui import QColor


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

        # Lista ficticia de elementos
        self.elementos = [
        #   {"Id":"1","Nombew Juicio":"P-412-2020","Afp":"HABITAT","Nombre": "SOCIEDAD EDUCACIONAL HELLEN KELLER LIMITADA, IVONNE YANETT GUTIERREZ POZO","Domicilio":"AVENIDA SAN RAMON 595, La Serena" ,"Notficada":True,"Estampada":False,"Rol":"Notificar demanda","Tipo":"NEGATIVA","Pagar":"12000"},
        #  {"Id":"2","Nombew Juicio":"P-412-2020","Afp":"HABITAT","Nombre": "SOCIEDAD EDUCACIONAL HELLEN KELLER LIMITADA, IVONNE YANETT GUTIERREZ POZO","Domicilio":"AVENIDA SAN RAMON 595, La Serena" ,"Notficada":False,"Estampada":True,"Rol":"Notificar demanda","Tipo":"NEGATIVA","Pagar":"12000"},
        # {"Id":"3","Nombew Juicio":"P-412-2020","Afp":"HABITAT","Nombre": "SOCIEDAD EDUCACIONAL HELLEN KELLER LIMITADA, IVONNE YANETT GUTIERREZ POZO","Domicilio":"AVENIDA SAN RAMON 595, La Serena" ,"Notficada":True,"Estampada":True,"Rol":"Notificar demanda","Tipo":"NEGATIVA","Pagar":"12000"},
        #{"Id":"4","Nombew Juicio":"P-412-2020","Afp":"HABITAT","Nombre": "SOCIEDAD EDUCACIONAL HELLEN KELLER LIMITADA, IVONNE YANETT GUTIERREZ POZO","Domicilio":"AVENIDA SAN RAMON 595, La Serena" ,"Notficada":False,"Estampada":False,"Rol":"Notificar demanda","Tipo":"NEGATIVA","Pagar":"12000"}
        ]
    def estampar_clicked(self):
        # Manejar la lógica cuando se hace clic en el botón de estampado
        button = self.sender()  # Obtener el botón que emitió la señal
        index = self.table.indexAt(button.pos())  # Obtener la posición del botón en la tabla
        row, col = index.row(), index.column()
        #llama a la ventana estampado
        self.estampado_app = estampado.EstampadoApp()
        self.estampado_app.show()
        
    def ingresar_clicked(self):
        # Conectar a la base de datos MySQL
        conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='',
            database='mi_causa'
        )

        # Crear un cursor
        cursor = conn.cursor()

        # Ejecutar una consulta SELECT
        query = "SELECT Id, Numerojuicio, AFP, Nombre, Domicilio, RolCausa, TipoCausa, Pagar FROM datoscausas"
        cursor.execute(query)

        # Obtener todos los resultados
        resultados = cursor.fetchall()

        # Lista que contendrá los diccionarios
        self.elementos = []

        # Iterar sobre los resultados y agregarlos al diccionario
        for fila in resultados:
            # Crear un diccionario para cada fila
            elemento = {
                "Id": fila[0],
                "Nombew_Juicio": fila[1],
                "Afp": fila[2],
                "Nombre": fila[3],
                "Domicilio": fila[4],
                "Rol": fila[5],
                "Tipo": fila[6],
                "Pagar": fila[7],
                "Notificada": True,#Se necesita cambiar esto segun de donde3 vengan estos datos de la bd
                "Estampada": True,#Se necesita cambiar esto segun de donde3 vengan estos datos de la bd
            }
            self.elementos.append(elemento)

        # Mostrar los diccionarios
        for elemento in self.elementos:
            print(elemento)

        # Cerrar el cursor y la conexión
        cursor.close()
        conn.close()
    def mostrar_clicked(self):
        self.table.setColumnCount(10)  # Número de columnas
        self.table.setHorizontalHeaderLabels(['Id', 'Numero de Juicio', 'AFP', 'Nombre','Domicilio','Rol Causa','Tipo Causa','Pagar','Notificada','Estampada'])  # Etiquetas de las columnas
        
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
