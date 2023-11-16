import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QTableWidget, \
    QTableWidgetItem, QHeaderView, QCheckBox, QHBoxLayout , QMessageBox
from PyQt6.QtGui import QColor
import pymssql
from funcionalidades.verCausa import VerCausaApp
from funcionalidades.buscado import BuscadorDatosCausaApp
from funcionalidades.insertar_excel import ExcelToDatabaseApp
from funcionalidades.insertar_manual import MiApp
from funcionalidades.estampadoV2  import EstampadoApp

class DashboardApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Dashboard App')
        self.setGeometry(100, 100, 830, 600)

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)
        self.layout_vertical = QVBoxLayout()  # Crea un layout vertical
        self.layout_horizontal = QHBoxLayout()  # Crea un layout horizontal

        # Crea botones
        self.crear_botones()

        # Añade botones al layout horizontal y el layout horizontal al layout vertical
        self.layout_horizontal.addWidget(self.btn_buscar)
        self.layout_horizontal.addWidget(self.btn_Insertar_excel)
        self.layout_horizontal.addWidget(self.btn_Insertar_manual)
        self.layout_vertical.addLayout(self.layout_horizontal)

        # Crea una tabla y un botón de guardar
        self.table = QTableWidget()
        self.layout_vertical.addWidget(self.table)
        self.btn_Guardar = QPushButton('Guardar', self)
        self.btn_Guardar.clicked.connect(self.Guardar_clicked)
        self.layout_vertical.addWidget(self.btn_Guardar)

        # Configuraciones finales del diseño
        self.central_widget.setLayout(self.layout_vertical)
        self.ajustar_tamanio()

        # Llama automáticamente a acceder_base_de_datos y mostrar_clicked al iniciar la aplicación
        self.establecer_conexion_base_de_datos()
        self.acceder_base_de_datos()
        self.mostrar_clicked()

    def crear_botones(self):
        self.btn_buscar = self.crear_boton('Buscar', self.buscar_clicked)
        self.btn_Insertar_excel = self.crear_boton('Insertar Excel', self.Insertar_excel_clicked)
        self.btn_Insertar_manual = self.crear_boton('Insertar Manual', self.Insertar_manual_clicked)

    def crear_boton(self, texto, funcion):
        boton = QPushButton(texto, self)
        boton.clicked.connect(funcion)
        return boton

    def establecer_conexion_base_de_datos(self):
        self.db_connection = pymssql.connect(
            server='vps-3697915-x.dattaweb.com',
            user='daniel',
            password='LOLxdsas--',
            database='micau5a'
        )

    def cerrar_conexion_base_de_datos(self):
        if self.db_connection:
            self.db_connection.close()

    def actualizar_base_de_datos(self, causa):
        print(causa)
        try:
            self.establecer_conexion_base_de_datos()
            with self.db_connection.cursor() as cursor:
                query = f"UPDATE notificacion SET [estadoCausa] = '{causa['Busqueda positiva']}' WHERE rolCausa = '{causa['Rol Causa']}'"
                cursor.execute(query)
            self.db_connection.commit()
            self.cerrar_conexion_base_de_datos()
            
        except Exception as e:
             print(e)
             QMessageBox.critical(self, "Error", "Error al guardar los datos")
        

    def acceder_base_de_datos(self):
        try:
            with self.db_connection.cursor() as cursor:
                query = "SELECT fechaNotificacion, numjui, nombmandante, nombDemandado, domicilio, rolCausa, arancel, nombTribunal, estadoCausa FROM notificacion"
                cursor.execute(query)
                resultados = cursor.fetchall()

            self.causas = []
            for fila in resultados:
                causa = {
                    "Fecha notificacion": fila[0],
                    "Rol": fila[1],
                    "Nombre Mandante": fila[2],
                    "Nombre Demandante": fila[3],
                    "Domicilio": fila[4],    
                    "Estado": fila[5],
                    "Arancel": fila[6],
                    "Tribunal": fila[7],
                    "Notificada": True,
                    "Estampada": True,
                    "VerCausa": "Ver Causa",
                    "Busqueda positiva": fila[8],
                    "Busqueda negativa": fila[8],
                }
                self.causas.append(causa)
            self.cerrar_conexion_base_de_datos()
        except Exception as e:
            print(f"Error al acceder a la base de datos: {e}")

    def mostrar_clicked(self):
        self.table.setColumnCount(16)
        self.table.setHorizontalHeaderLabels(['Fecha',  'Rol', 'Nombre mandante', 'Nombre demandante', 'Domicilio', 'Estado', 'Arancel', 'Tribunal', 'Notificada',
                                              'Estampada', 'Ver Causa', 'Busqueda Positiva', 'Busqueda Negativa'])

        for row_index, causa in enumerate(self.causas):
            self.table.insertRow(row_index)
            notificada = causa["Notificada"]
            estampada = causa["Estampada"]

            for col_index, (key, value) in enumerate(causa.items()):
                item = QTableWidgetItem(str(value))

                if key == "Estampada":
                    button = self.crear_boton("Estampar", self.estampar_clicked)
                    self.table.setCellWidget(row_index, col_index, button)
                elif key == "VerCausa":
                    button = self.crear_boton("Ver Causa", self.verCausa_clicked)
                    self.table.setCellWidget(row_index, col_index, button)
                elif key in ["Busqueda positiva", "Busqueda negativa"]:
                    checkbox = QCheckBox("Si" if value == 1 else "No", self)
                    checkbox.setChecked(bool(value))
                    self.table.setCellWidget(row_index, col_index, checkbox)

                self.color_y_etiqueta_celda(item, estampada, notificada)
                self.table.setItem(row_index, col_index, item)

        self.ajustar_tamanio()

    def Guardar_clicked(self):
        for row_index, causa in enumerate(self.causas):
            checkbox_positiva = self.table.cellWidget(row_index, 7)
            checkbox_negativa = self.table.cellWidget(row_index, 8)
            causa["Busqueda positiva"] = "1" if checkbox_positiva.isChecked() else "0"
            causa["Busqueda positiva"] = "0" if checkbox_negativa.isChecked() else "1"
            causa["Busqueda negativa"] = "1" if checkbox_negativa.isChecked() else "0"
            causa["Busqueda negativa"] = "0" if checkbox_positiva.isChecked() else "1"
            self.actualizar_base_de_datos(causa)
        QMessageBox.information(self, "Exito", "Datos guardados correctamente")
    def Insertar_excel_clicked(self):
        # Lógica para insertar desde Excel
        self.exc = ExcelToDatabaseApp()
        self.exc.show()

    def Insertar_manual_clicked(self):
        # Lógica para insertar manualmente
        self.exa = MiApp()
        self.exa.show()

    def estampar_clicked(self):
        # logicas para estampar
        self.ex3 = EstampadoApp()
        self.ex3.show()

    def buscar_clicked(self):
        # Lógica para buscar
        self.bas = BuscadorDatosCausaApp()
        self.bas.show()

    def verCausa_clicked(self):
        button = self.sender()
        index = self.table.indexAt(button.pos())
        row, col = index.row(), index.column()
        causa = self.causas[row]
        self.vercausa_app = VerCausaApp(causa)
        self.vercausa_app.show()

    def ajustar_tamanio(self):
        self.table.resizeColumnsToContents()
        total_width = sum(self.table.columnWidth(col) for col in range(self.table.columnCount()))
        min_width = max(self.width(), total_width)
        self.setMinimumWidth(min_width)
        self.adjustSize()

    def color_y_etiqueta_celda(self, item, estampada, notificada):
        color = QColor()
        if estampada and notificada:
            color = QColor(0, 255, 0)  # Verde
        elif estampada and not notificada:
            color = QColor(255, 255, 0)  # Amarillo
        elif not estampada and notificada:
            color = QColor(0, 0, 255)  # Azul
        else:
            color = QColor(255, 0, 0)  # Rojo
        item.setBackground(color)


def main():
    app = QApplication(sys.argv)
    window = DashboardApp()
    window.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
