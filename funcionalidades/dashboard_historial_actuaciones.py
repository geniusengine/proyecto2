import sys
import time
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QTableWidget, \
    QTableWidgetItem, QHeaderView, QCheckBox, QHBoxLayout , QMessageBox, QLabel,QComboBox, QToolButton, QMenu
from PyQt6.QtGui import QColor, QIcon
from PyQt6.QtCore import QDateTime, QTimer, Qt, pyqtSignal
import pymssql

from estampado_app import Estampadoxd



class DashboardHistorialActuaciones(QMainWindow):
    def __init__(self):


        super().__init__()
        self.db_connection = None
        self.datos = []
        self.initUI()
        print("Dashboard Actuaciones")
    
    def initUI(self):
        self.setWindowTitle('Historial Actuaciones')
        self.setWindowIcon(QIcon("static/icons/icono-ventana.png"))
        self.setGeometry(100, 100, 1280, 720)

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)
        self.layout_vertical = QVBoxLayout()  # Crea un layout vertical
        self.layout_horizontal = QHBoxLayout()  # Crea un layout horizontal
   
        self.layout_horizontal.addLayout(self.layout_vertical)# Agrega el layout vertical al layout horizontal

        # Crea una tabla y un botón de guardar
        self.table = QTableWidget()
        # Establecer el color de las líneas de las celdas
        self.table.setStyleSheet(
        "QTableView { gridline-color: white; }"
        "QTableCornerButton::section { background-color: #d3d3d3; border: 1px solid black; }"
        "QHeaderView::section { background-color: #d3d3d3; border: 1px solid black; }"
        )
        self.layout_vertical.addWidget(self.table)# Agrega la tabla al layout vertical
    
        # Conectar la señal de clic en el encabezado de la columna para ordenar
        self.table.horizontalHeader().sectionClicked.connect(self.ordenar_tabla)

        # Configuraciones finales del diseño
        self.central_widget.setLayout(self.layout_horizontal)

        # Llama automáticamente a acceder_base_de_datos y mostrar_clicked al iniciar la aplicación
        self.establecer_conexion_base_de_datos()
        self.obtener_datos()
        self.mostrar_tabla()

        self.setGeometry(100, 100, 400, 300)


    def combo_box_changed(self, row, col, index):
        # Aquí deberías escribir el código que se ejecutará cuando cambie el índice del combo box
        pass

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
        max_width = 1000  # Puedes ajustar este valor según tus necesidades
        min_width = min(min_width, max_width)
        
        self.setMinimumWidth(min_width - 260)
        self.setMaximumWidth(max_width)  # Establecer un ancho máximo para la ventana
        self.adjustSize()
    # ...
    def establecer_conexion_base_de_datos(self):
        try:
            self.db_connection = pymssql.connect(
                server='vps-3697915-x.dattaweb.com',
                user='daniel',
                password='LOLxdsas--',
                database='micau5a'
            )
        except Exception as e:
            print(f"Error al establecer la conexión: {e}")

    def cerrar_conexion_base_de_datos(self):
        try:
            if self.db_connection:
                self.db_connection.close()
        except Exception as e:
            print(f"Error al cerrar la conexión: {e}")

    def obtener_datos(self):
        
        try:
            self.establecer_conexion_base_de_datos()
            with self.db_connection.cursor() as cursor:
                query = "SELECT fechaNotificacion, numjui, nombTribunal, nombdemandante, apellidemandante, demandado, repre, mandante, domicilio, comuna, encargo, soli, arancel, estadoNoti, estadoCausa FROM AUD_notificacion"
                
        
                
                cursor.execute(query)
                resultados = cursor.fetchall()
                
                
            self.causas=[]
            for fila in resultados:
                causa = {'fechaNotificacion':fila[0],'numjui':fila[1],'nombtribunal':fila[2],'nomdemandante':fila[3],'apellidemandante':fila[4],'demandado':fila[5],'repre':fila[6],'mandante':fila[7],'domicilio':fila[8],'comuna':fila[9],'encargo':fila[10],'soli':fila[11],'arancel':fila[12],'Estampar':fila[13],}
                    
                
                self.causas.append(causa)
        except Exception as e:
            print(f"Error al acceder a la base de datos: {e}")
        finally:
            self.cerrar_conexion_base_de_datos()

# ...

        
# muestra los datos en la tabla
    def mostrar_tabla(self):
        self.table.setColumnCount(15)
        self.table.setHorizontalHeaderLabels(['fechaNotificacion', 'Rol', 'Tribunal', 'Nombre demandante', 'Apellido demandante', 'Nombre demandado', 'Representante', 'Quien Encarga', 'Domicilio', 'Comuna', 'Encargo', 'Resultado', 'Arancel',  'Estampar','Actuación'])
        for row_index, causa in enumerate(self.causas):
            
            self.table.insertRow(row_index)
            for col_index, (key, value) in enumerate(causa.items()):
                        if key == "Estampar":
                            button = self.crear_boton_con_icono("static/icons/firmar.png", self.estampar_clicked)
                            self.table.setCellWidget(row_index, col_index, button)
                        elif key == "Actuación":
                        # Crear un objeto QComboBox para las celdas de actuaciones
                            combo_box = QComboBox()
                            opciones_actuaciones = ["Elija actuación", "Búsqueda Negativa", "Búsqueda Positiva", "Not. por cédula", "Not. Art. 44", "Req. de pago en Oficina", "Op. al Embargo", "Not. Personal", "Not. Personal/Req. de Pago", "Not. art. 52", "Embargo con Fuerza Pública", "Embargo Frustrado", "Embargo Banco", "Embargo Vehículo", "Retiro de Vehículo", "Retiro Frustrado", "Retiro de Especies ", "OtrO"]
                            combo_box.addItems(opciones_actuaciones)
                            combo_box.setCurrentText(value)
                            self.table.setCellWidget(row_index, col_index, combo_box)
                            combo_box.currentIndexChanged.connect(lambda index, row=row_index, col=col_index: self.combo_box_changed(row, col, index))
                        elif key == "Tipo de Juicio":
                        # Crear un objeto QComboBox para las celdas de tipo de juicio
                            combo_box = QComboBox()
                            opciones_tipojuicio = ["Elija tipo de juicio", "Ejecutivo", "Ordinario"]
                            combo_box.addItems(opciones_tipojuicio)
                            combo_box.setCurrentText(value)
                            self.table.setCellWidget(row_index, col_index, combo_box)
                            combo_box.currentIndexChanged.connect(lambda index, row=row_index, col=col_index: self.combo_box_changed(row, col, index))
                        else:
                        # Crea un objeto QTableWidgetItem para las otras columnas
                            item = QTableWidgetItem(str(value))
                        # establece el color de la celda
                            item.setBackground(QColor(52, 152, 219))
                            self.table.setItem(row_index, col_index, item)
                    
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
            apellidemandante = self.table.item(selected_row,4).text()  
            demandado = self.table.item(selected_row, 5).text()  
            repre = self.table.item(selected_row, 6).text()  
            mandante = self.table.item(selected_row,7).text()  
            domicilio = self.table.item(selected_row, 8).text()  
            comuna = self.table.item(selected_row, 9).text()  
            encargo = self.table.item(selected_row, 10).text() 
            soli = self.table.item(selected_row, 11).text() 
            arancel = self.table.item(selected_row, 12).text() 

            # Importa Estampadoxd localmente
            self.ex3 = Estampadoxd(fechaNotificacion, numjui, nombTribunal, nombdemandante, apellidemandante, demandado, repre, mandante, domicilio, comuna, encargo, soli, arancel)
            self.ex3.show()

            button = self.sender()
            index = self.table.indexAt(button.pos())
            row, col = index.row(), index.column()
            causa = self.causas[row]

            # Verifica si la causa ya ha sido notificada
            numjui = self.table.item(selected_row, 4).text()


       
        
    
       
   
# Ejecuta la función principal
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = DashboardHistorialActuaciones()
    window.show()
    sys.exit(app.exec())

   