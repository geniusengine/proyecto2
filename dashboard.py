import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QTableWidget, QTableWidgetItem, QFileDialog, QMessageBox
import pandas as pd
import mysql.connector
import estampado
from PyQt6.QtGui import QColor


class Dashboard(QMainWindow):
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
            {"Id":"1","Nombew Juicio":"P-412-2020","Afp":"HABITAT","Nombre": "SOCIEDAD EDUCACIONAL HELLEN KELLER LIMITADA, IVONNE YANETT GUTIERREZ POZO","Domicilio":"AVENIDA SAN RAMON 595, La Serena" ,"Notficada":True,"Estampada":False,"Rol":"Notificar demanda","Tipo":"NEGATIVA","Pagar":"12000"},
            {"Id":"2","Nombew Juicio":"P-412-2020","Afp":"HABITAT","Nombre": "SOCIEDAD EDUCACIONAL HELLEN KELLER LIMITADA, IVONNE YANETT GUTIERREZ POZO","Domicilio":"AVENIDA SAN RAMON 595, La Serena" ,"Notficada":False,"Estampada":True,"Rol":"Notificar demanda","Tipo":"NEGATIVA","Pagar":"12000"},
            {"Id":"3","Nombew Juicio":"P-412-2020","Afp":"HABITAT","Nombre": "SOCIEDAD EDUCACIONAL HELLEN KELLER LIMITADA, IVONNE YANETT GUTIERREZ POZO","Domicilio":"AVENIDA SAN RAMON 595, La Serena" ,"Notficada":True,"Estampada":True,"Rol":"Notificar demanda","Tipo":"NEGATIVA","Pagar":"12000"},
            {"Id":"4","Nombew Juicio":"P-412-2020","Afp":"HABITAT","Nombre": "SOCIEDAD EDUCACIONAL HELLEN KELLER LIMITADA, IVONNE YANETT GUTIERREZ POZO","Domicilio":"AVENIDA SAN RAMON 595, La Serena" ,"Notficada":False,"Estampada":False,"Rol":"Notificar demanda","Tipo":"NEGATIVA","Pagar":"12000"}

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
    # muestra los datos en la tabla cargada desde el archivo excel
    def mostrar_clicked(self):
        self.table.setColumnCount(10)  # Número de columnas
        self.table.setHorizontalHeaderLabels(['Id', 'Numero de Juicio', 'AFP', 'Nombre','Domicilio','Notificada','Estampada','Rol Causa','Tipo Causa','Pagar'])  # Etiquetas de las columnas
        
        #
        for row_index, elemento in enumerate(self.elementos):#row_index es el indice de la fila y segun los elementos que haya en la lista elementos se crean las filas
            self.table.insertRow(row_index)#inserta al final de la tabla una fila
    
            for col_index, (key, value) in enumerate(elemento.items()):#col_index es el indice de la columna
                item = QTableWidgetItem(str(value))#crea un item con el valor de la celda
                #establecer un boton en la celda de estampado
                if key == "Estampada":
                    button = QPushButton("Estampar", self)
                    button.clicked.connect(self.estampar_clicked)
                    self.table.setCellWidget(row_index, col_index, button)

                # Definir colores según el estado de notificación y estampado
                if key == "Notificada" and value:#si la notificacion es verdadera 
                    #no se metera nunca abajo ya que solo esta recorriendo un valor a la vez a menos que se recorra con 2 for
                    item.setBackground(QColor(0, 255, 0))  # Verde
                    #if notificada y estampada son verdaderas
                    if key == "Estampada" and value:# estampado es verdadero
                        item.setBackground(QColor(0, 255, 255))  # Verde
                        
                        self.table.setVerticalHeaderLabels(['Verde'])#etiqueta la fila
                    #if notificada es verdadera y estampada es falsa
                    elif key == "Estampada" and not value:
                        item.setBackground(QColor(255, 0, 0)) #azul
                        self.table.setVerticalHeaderLabels(['Azul'])#etiqueta la fila

                elif key == "Notificada" and not value:
                    #if notificada es falsa y estampada es falsa
                    item.setBackground(QColor(255, 0, 0))  # Rojo
                    self.table.setVerticalHeaderLabels(['Rojo'])#etiqueta la fila

                #funciona
                if key == "Estampada" and value:
                    #if notificada es falsa y estampada es verdadera
                    item.setBackground(QColor(0, 0, 255))  # Azul
                    self.table.setVerticalHeaderLabels(['Azul'])#etiqueta la fila

                elif key == "Estampada" and not value:
                    #if notificada es verdadera y estampada es falsa
                    item.setBackground(QColor(255, 0, 255))  # Blanco
                    self.table.setVerticalHeaderLabels(['Blanco'])#etiqueta la fila

                self.table.setItem(row_index, col_index, item)

def main():
    app = QApplication(sys.argv)
    window = DashboardApp()
    window.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
