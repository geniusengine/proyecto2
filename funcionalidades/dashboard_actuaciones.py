import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QTableWidget, \
    QTableWidgetItem, QHeaderView, QCheckBox, QHBoxLayout , QMessageBox, QLabel,QComboBox
from PyQt6.QtGui import QColor, QIcon
from PyQt6.QtCore import QDateTime, QTimer, Qt, pyqtSignal
import pymssql

from estampado_app import Estampadoxd


class Dashboard_actuacionesApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.db_connection = None
        self.initUI()
    
    def initUI(self):
        self.setWindowTitle('Dashboard App')
        self.setGeometry(100, 100, 1280, 720)

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)
        self.layout_vertical = QVBoxLayout()  # Crea un layout vertical
        self.layout_horizontal = QHBoxLayout()  # Crea un layout horizontal
   
        self.layout_vertical.addLayout(self.layout_horizontal)

        # Crea una tabla y un botón de guardar
        self.table = QTableWidget()
        # Establecer el color de las líneas de las celdas
        self.table.setStyleSheet(
        "QTableView { gridline-color: white; }"
        "QTableCornerButton::section { background-color: #d3d3d3; border: 1px solid black; }"
        "QHeaderView::section { background-color: #d3d3d3; border: 1px solid black; }"
        )
        self.layout_vertical.addWidget(self.table)
    
        # Conectar la señal de clic en el encabezado de la columna para ordenar
        self.table.horizontalHeader().sectionClicked.connect(self.ordenar_tabla)

        # Configuraciones finales del diseño
        self.central_widget.setLayout(self.layout_vertical)

        # Llama automáticamente a acceder_base_de_datos y mostrar_clicked al iniciar la aplicación
        self.establecer_conexion_base_de_datos()
        self.mostrar_tabla()

        self.setGeometry(100, 100, 400, 300)

    # crea cada boton que se necesite
    def crear_boton(self, texto, funcion):
        boton = QPushButton(texto, self)
        boton.clicked.connect(funcion)
        return boton
    # crea un boton con un icono
    def crear_boton_con_icono(self, icono_path, funcion):
        boton = QPushButton(self)
        icono = QIcon(icono_path)
        boton.setIcon(icono)
        boton.clicked.connect(funcion)
        return boton
    
    def update_dashboard(self):
        # Esta función se llamará cuando se guarden los datos
        self.label.setText("¡Panel Actualizado!")
        
        
    # establece la conexion con la base de datos
    def establecer_conexion_base_de_datos(self):
        self.db_connection = pymssql.connect(
            server='vps-3697915-x.dattaweb.com',
            user='daniel',
            password='LOLxdsas--',
            database='micau5a'
        )
    # cierra la conexion con la base de datos
    def cerrar_conexion_base_de_datos(self):
        if self.db_connection:
            self.db_connection.close()


# limpia la tabla
    def limpiar_tabla(self):
        self.table.clearContents()
        self.table.setRowCount(0)
# obtiene la fecha actual
    def obtener_fecha_actual(self):
        # Obtener la fecha y hora actual
        fecha_actual = QDateTime.currentDateTime()
        # Formatear la fecha y hora
        formato_fecha = fecha_actual.toString('yyyy-MM-dd HH:mm:ss')
        return formato_fecha
# ajusta el tamaño de la tabla ajustándose al contenido
    def ajustar_tamanio(self):
        self.table.resizeColumnsToContents()
        total_width = sum(self.table.columnWidth(col) for col in range(self.table.columnCount()))
        min_width = max(self.width(), total_width)
        
        # Establecer un ancho máximo para la ventana
        max_width = 800  # Puedes ajustar este valor según tus necesidades
        min_width = min(min_width, max_width)
        
        self.setMinimumWidth(min_width - 375)
        self.setMaximumWidth(max_width)  # Establecer un ancho máximo para la ventana
        self.adjustSize()
# muestra los datos en la tabla
    def mostrar_tabla(self):
        causa = {"fecha": "FechaPrueba",
                "rol": "Rolprueba",
                "tribunal": "Tribunalprueba",
                "actuacion": "Actuacionprueba",
                "tipojuicio": "Tipojuicioprueba",
                "Estampada": "Estampada"}
        print(causa)
        self.causas = []
        self.causas.append(causa)
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(['Fecha',  'Rol', 'Tribunal','Actuacion','Tipo de juicio','Estampar'])
        for row_index, causa in enumerate(self.causas):
            self.table.insertRow(row_index)
            for col_index, (key, value) in enumerate(causa.items()):
                if key == "Estampada":
                    button = self.crear_boton_con_icono("static/icons/firmar.png", self.estampar_clicked)
                    self.table.setCellWidget(row_index, col_index, button)
                elif key == "actuacion":
                    # Crear un objeto QComboBox para las celdas de actuaciones
                    combo_box = QComboBox()
                    opciones_actuaciones = ["Opción 1", "Opción 2", "Opción 3"]  # Puedes personalizar las opciones
                    combo_box.addItems(opciones_actuaciones)
                    combo_box.setCurrentText(value)
                    self.table.setCellWidget(row_index, col_index, combo_box)
                elif key == "tipojuicio":
                    # Crear un objeto QComboBox para las celdas de tipo de juicio
                    combo_box = QComboBox()
                    opciones_tipojuicio = ["Opción 1", "Opción 2", "Opción 3"]
                    combo_box.addItems(opciones_tipojuicio)
                    combo_box.setCurrentText(value)
                    self.table.setCellWidget(row_index, col_index, combo_box)
                else:
                    # Crea un objeto QTableWidgetItem para las otras columnas
                    item = QTableWidgetItem(str(value))
                    #establece el color de la celda
                    item.setBackground(QColor(26, 26, 255))
                    self.table.setItem(row_index, col_index, item)  
                    print(key, value)
        self.ajustar_tamanio()
# Función para ordenar la tabla según la columna clicada
    def ordenar_tabla(self, logicalIndex):
        self.table.sortItems(logicalIndex, Qt.SortOrder.AscendingOrder if self.table.horizontalHeader().sortIndicatorOrder() == Qt.SortOrder.DescendingOrder else Qt.SortOrder.DescendingOrder)
        
# abre la ventana de estampado
    def estampar_clicked(self):
        # Obtener la fila seleccionada
        selected_row = self.table.currentRow()
        # Verificar si se seleccionó una fila
        if selected_row != -1:
            # Obtener datos de la fila seleccionada
            fechaNotificacion = self.table.item(selected_row, 0).text()
            numjui = self.table.item(selected_row, 1).text()
            nombTribunal = self.table.item(selected_row, 2).text()
            nombdemandante = self.table.item(selected_row, 3).text()
            apellidemandante = self.table.item(selected_row, 4).text()
            demandado = self.table.item(selected_row, 5).text()
            repre = self.table.item(selected_row, 6).text()
            mandante = self.table.item(selected_row, 7).text()
            domicilio = self.table.item(selected_row, 8).text()
            comuna = self.table.item(selected_row, 9).text()
            encargo = self.table.item(selected_row, 10).text()
            soli = self.table.item(selected_row, 11).text()
            arancel = self.table.item(selected_row, 12).text()
    
            #observacion = self.table.item(selected_row, 17).text()
            #########################################################################################Observacion agreagr ??????????????
            # Importa Estampadoxd localmente
            self.ex3 = Estampadoxd(fechaNotificacion, numjui, nombTribunal, nombdemandante, apellidemandante, demandado, repre, mandante, domicilio, comuna, encargo, soli, arancel)
            self.ex3.show()
        
        button = self.sender()
        index = self.table.indexAt(button.pos())
        row, col = index.row(), index.column()
        causa = self.causas[row]
        color = QColor(250, 193, 114)

        # Verifica si la causa ya ha sido notificada
        if causa["Estampada"] == 1:
            QMessageBox.warning(self, "Advertencia", "Esta causa ya ha sido notificada.")
            return
        
        # Actualiza la información localmente
        causa["Estampada"] = 1
        
        # Actualiza el valor en la base de datos
        try:
            self.establecer_conexion_base_de_datos()
            with self.db_connection.cursor() as cursor:
                query = f"UPDATE notificacion SET estadoCausa = 1"
                cursor.execute(query)
            self.db_connection.commit()
        except pymssql.Error as db_error:
            print(f"Error al ejecutar la consulta SQL: {db_error}")
            self.db_connection.rollback()
            raise  # Re-levanta la excepción para que el programa no continúe si hay un error grave en la base de datos
        except Exception as e:
            print(f"Error desconocido: {e}")
            raise  # Re-levanta la excepción para que el programa no continúe si hay un error desconocido
        finally:
            self.cerrar_conexion_base_de_datos()
        # Actualiza la celda en la tabla y el color de la fila
        self.actualizar_color_fila(row)
        # Proporciona un mensaje de éxito al usuario
# Función principal
def main():
    app = QApplication(sys.argv)
    window = Dashboard_actuacionesApp()
    

    window.show()
    sys.exit(app.exec())
    
# Ejecuta la función principal
if __name__ == '__main__':
    main()