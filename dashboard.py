import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QTableWidget, QTableWidgetItem
from PyQt6.QtGui import QColor
import pymssql
from verCausa import VerCausaApp

class DashboardApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Dashboard App')
        self.setGeometry(100, 100, 860, 600)

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()

        self.table = QTableWidget()
        self.layout.addWidget(self.table)

        #crea un boton para buscar
        self.btn_buscar = QPushButton('Buscar', self)
        self.btn_buscar.clicked.connect(self.buscar_clicked)
        self.layout.addWidget(self.btn_buscar)
         

        self.central_widget.setLayout(self.layout)

        # Llama automáticamente a acceder_base_de_datos y mostrar_clicked al iniciar la aplicación
        self.acceder_base_de_datos()
        self.mostrar_clicked()

    def estampar_clicked(self):
        # Manejar la lógica cuando se hace clic en el botón de estampado
        pass
    
    def buscar_clicked(self):
        import subprocess
        subprocess.Popen(['python', 'buscado.py'])

        pass

    def verCausa_clicked(self):
        # Manejar la lógica cuando se hace clic en el botón de VerCausa
        button = self.sender()
        index = self.table.indexAt(button.pos())
        row, col = index.row(), index.column()
        # Obtener la causa correspondiente a la fila
        causa = self.causas[row]
        # Llama a la ventana VerCausa
        self.vercausa_app = VerCausaApp(causa)
        self.vercausa_app.show()

    def acceder_base_de_datos(self):
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
        query = "SELECT fechaNotificacion, rutDemandado, rutMandante, rolCausa, nombTribunal, notificacion FROM notificacion"
        cursor.execute(query)

        # Obtener todos los resultados
        resultados = cursor.fetchall()

        # Cerrar el cursor y la conexión
        cursor.close()
        conn.close()

        self.causas = []

        for fila in resultados:
            causa = {
                "Fecha": fila[0],
                "Rut Demandado": fila[1],
                "Rut Mandante": fila[2],
                "Rol Causa": fila[3],
                "Tribunal": fila[4],
                "Notificada": fila[5],
                "Estampada": True,
                "VerCausa": True,
            }
            self.causas.append(causa)

    def mostrar_clicked(self):
        self.table.setColumnCount(8)  # Número de columnas
        self.table.setHorizontalHeaderLabels(['Fecha', 'Rut demandado', 'Rut mandante', 'Rol Causa', 'Tribunal', 'notificada', 'Estampada', 'Ver Causa'])  # Etiquetas de las columnas

        for row_index, causa in enumerate(self.causas):
            self.table.insertRow(row_index)
            notificada = causa["Notificada"]
            estampada = causa["Estampada"]
            for col_index, (key, value) in enumerate(causa.items()):
                item = QTableWidgetItem(str(value))
                # Establecer un botón en la celda de estampado
                if key == "Estampada":
                    button = QPushButton("Estampar", self)
                    button.clicked.connect(self.estampar_clicked)
                    self.table.setCellWidget(row_index, col_index, button)
                # Establecer un botón en la celda de ver causa
                elif key == "VerCausa":
                    button = QPushButton("Ver Causa", self)
                    button.clicked.connect(self.verCausa_clicked)
                    self.table.setCellWidget(row_index, col_index, button)

                self.color_y_etiqueta_celda(item, estampada, notificada)
                self.table.setItem(row_index, col_index, item)

    def color_y_etiqueta_celda(self, item, estampada, notificada):
        color = QColor()

        if estampada and notificada:
            color = QColor(0, 255, 0)  # Verde
            etiqueta = 'Verde'
        elif estampada and not notificada:
            color = QColor(255, 255, 0)  # Amarillo
            etiqueta = 'Amarillo'
        elif not estampada and notificada:
            color = QColor(0, 0, 255)  # Azul
            etiqueta = 'Azul'
        else:
            color = QColor(255, 0, 0)  # Rojo
            etiqueta = 'Rojo'

        item.setBackground(color)
        self.table.setVerticalHeaderLabels([etiqueta])

def main():
    app = QApplication(sys.argv)
    window = DashboardApp()
    window.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
