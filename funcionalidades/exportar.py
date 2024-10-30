import os
import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QTableWidget, \
    QTableWidgetItem, QHeaderView, QCheckBox, QHBoxLayout, QMessageBox, QLabel, QLineEdit, QFileDialog
from PyQt6.QtGui import QColor, QIcon
from PyQt6.QtCore import QDateTime, QTimer, Qt, pyqtSignal
import mysql.connector
import pandas as pd
import logging
from datetime import datetime

# Configurar el sistema de registro
logging.basicConfig(filename='registro.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class exportN(QMainWindow):
    datos_actualizados_signal = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.db_connection = None
        self.initUI()
    
    def initUI(self):
        self.setWindowTitle('Exportar Datos')
        self.setWindowIcon(QIcon("static/icono-ventana.png"))
        self.setGeometry(100, 100, 1280, 720)
        self.primer_mostrado = True

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)
        self.layout_vertical = QVBoxLayout()
        self.layout_horizontal = QHBoxLayout()

        # Temporizador para actualizar los datos cada 4 minutos
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.actualizar_datos)
        self.timer.start(240000)

        # Filtros
        self.txt_filtro_comuna = QLineEdit(self)
        self.txt_filtro_mandante = QLineEdit(self)
        self.btn_aplicar_filtro = QPushButton("Aplicar Filtro", self)
        self.btn_aplicar_filtro.clicked.connect(self.aplicar_filtro)

        filtro_layout = QHBoxLayout()
        filtro_layout.addWidget(QLabel("Filtrar por Comuna:"))
        filtro_layout.addWidget(self.txt_filtro_comuna)
        filtro_layout.addWidget(QLabel("Filtrar por Mandante:"))
        filtro_layout.addWidget(self.txt_filtro_mandante)
        filtro_layout.addWidget(self.btn_aplicar_filtro)
        self.layout_vertical.addLayout(filtro_layout)

        # Crear botones
        self.crear_botones()

        self.layout_vertical.addWidget(self.btn_exportar)
        self.layout_vertical.addLayout(self.layout_horizontal)

        # Crear una tabla
        self.table = QTableWidget()
        self.table.setStyleSheet(
            "QTableView { gridline-color: white; }"
            "QTableCornerButton::section { background-color: #d3d3d3; border: 1px solid black; }"
            "QHeaderView::section { background-color: #d3d3d3; border: 1px solid black; }"
        )
        
        self.layout_vertical.addWidget(self.table)
    
        self.table.horizontalHeader().sectionClicked.connect(self.ordenar_tabla)

        # Configuraciones finales
        self.central_widget.setLayout(self.layout_vertical)
        self.ajustar_tamanio()

        # Conexión y muestra inicial de datos
        self.establecer_conexion_base_de_datos()
        self.acceder_base_de_datos()
        self.mostrar_clicked()

        # Temporizador para eliminación y respaldo cada 10 minutos
        self.timer_eliminar_respaldo = QTimer(self)
        self.timer_eliminar_respaldo.timeout.connect(self.eliminar_y_respaldo)
        self.timer_eliminar_respaldo.start(1800000)

    def ajustar_tamanio(self):
        self.table.resizeColumnsToContents()
        total_width = sum(self.table.columnWidth(col) for col in range(self.table.columnCount()))
        min_width = max(self.width(), total_width) - 70
        self.setMinimumWidth(min_width)
        self.adjustSize()

    def color_y_etiqueta_celda(self, item, estampada, notificada):
        if item is not None:
            if notificada == 1 and estampada == 1:
                color = QColor(46, 204, 113)  # verde
            elif notificada == 0 and estampada == 1:
                color = QColor(250, 193, 114)  # amarillo
            else:
                color = QColor(224, 92, 69)  # rojo
            item.setBackground(color)


    def crear_botones(self):
        self.btn_exportar = self.crear_boton('Exportar', self.exportar_clicked)

    def aplicar_filtro(self):
        filtro_comuna = self.txt_filtro_comuna.text()
        filtro_mandante = self.txt_filtro_mandante.text()

        self.limpiar_tabla()
        self.establecer_conexion_base_de_datos()
        self.acceder_base_de_datos(filtro_comuna, filtro_mandante)
        self.mostrar_clicked()
        self.cerrar_conexion_base_de_datos()

    def crear_boton(self, texto, funcion):
        boton = QPushButton(texto, self)
        boton.clicked.connect(funcion)
        return boton
    
    def establecer_conexion_base_de_datos(self):
        try:
            self.db_connection = mysql.connector.connect(
                host='causas.mysql.database.azure.com', 
                user='admin_carlos',
                password='F14tomcat',
                database='matias1'
            )
            if self.db_connection.is_connected():
                print("Conexión a la base de datos MySQL establecida.")
        except mysql.connector.Error as e:
            print(f"Error al conectar a la base de datos MySQL: {e}")
            sys.exit(1)

    def cerrar_conexion_base_de_datos(self):
        if self.db_connection.is_connected():
            self.db_connection.close()

    def eliminar_y_respaldo(self):
        try:
            self.establecer_conexion_base_de_datos()
            cursor = self.db_connection.cursor()
            delete_query = "DELETE FROM notificacion WHERE estadoNoti = 1 and estadoCausa = 1"
            cursor.execute(delete_query)
            self.db_connection.commit()
        except mysql.connector.Error as db_error:
            print(f"Error al ejecutar la consulta SQL: {db_error}")
            self.db_connection.rollback()
        finally:
            self.cerrar_conexion_base_de_datos()

    def acceder_base_de_datos(self, filtro_comuna=None, filtro_mandante=None):
        try:
            cursor = self.db_connection.cursor()
            query = "SELECT fechaNotificacion, numjui, nombTribunal, demandante, demandado, repre, mandante, domicilio, comuna, encargo, soli, arancel, estadoNoti, estadoCausa FROM notificacion"
            
            if filtro_comuna:
                query += f" WHERE comuna = '{filtro_comuna}'"
            if filtro_mandante:
                query += f" AND mandante = '{filtro_mandante}'" if filtro_comuna else f" WHERE mandante = '{filtro_mandante}'"
            
            cursor.execute(query)
            resultados = cursor.fetchall()

            self.causas = []
            for fila in resultados:
                fecha_formateada = fila[0].strftime("%d-%m-%Y") if len(fila) > 0 else "Fecha no disponible"
                causa = {
                    "Fecha notificacion": fecha_formateada,
                    "Rol": fila[1],
                    "Tribunal": fila[2],
                    "demandante": fila[3],
                    "demandado": fila[4],
                    "repre": fila[5],
                    "mandante": fila[6],
                    "Domicilio": fila[7],
                    "Comuna": fila[8],
                    "Encargo": fila[9],
                    "Resultado": fila[10],
                    "Arancel": fila[11],
                    "Notificada": fila[12],
                    "estadoCausa": fila[13],
                }
                self.causas.append(causa)
            self.cerrar_conexion_base_de_datos()
        except mysql.connector.Error as db_error:
            print(f"Error al ejecutar la consulta SQL: {db_error}")
            self.db_connection.rollback()

    def limpiar_tabla(self):
        self.table.clearContents()
        self.table.setRowCount(0)

    def mostrar_clicked(self):
        self.table.setColumnCount(12)
        self.table.setHorizontalHeaderLabels(['Fecha notificacion', 'Rol', 'Tribunal', 'Demandante', 'Demandando', 'Representante', 'Mandante', 'Domicilio', 'Comuna', 'Encargo', 'Resultado', 'Arancel'])
        for row_index, causa in enumerate(self.causas):
            self.table.insertRow(row_index)
            notificada = causa["Notificada"]
            estampada = causa["estadoCausa"]
            for col_index, (key, value) in enumerate(causa.items()):
                item = QTableWidgetItem(str(value))
                self.table.setItem(row_index, col_index, item)
                self.color_y_etiqueta_celda(self.table.item(row_index, col_index), estampada, notificada)
        self.primera_vez()

    def exportar_clicked(self):
        selected_folder = QFileDialog.getExistingDirectory(self, "Selecciona la carpeta para guardar el archivo")
        if selected_folder:
            now = datetime.now()
            años = now.strftime("%d-%m-%y")
            try:
                df = pd.DataFrame(self.causas)
                columnas_deseadas = ['Fecha notificacion', 'Rol', 'Tribunal', 'demandante', 'demandado', 'repre', 'mandante', 'Domicilio', 'Comuna', 'Encargo', 'Resultado', 'Arancel']
                df_seleccionado = df.loc[:, columnas_deseadas]
                ruta_archivo = os.path.join(selected_folder, f'Nomina {años}.xlsx')
                df_seleccionado.to_excel(ruta_archivo, index=False)
                QMessageBox.information(self, "Información", "Los datos se han exportado correctamente.")
            except Exception as e:
                QMessageBox.warning(self, "Advertencia", f"Error al exportar a Excel: {e}")

    def ordenar_tabla(self, logicalIndex):
        self.table.sortItems(logicalIndex, Qt.SortOrder.AscendingOrder if self.table.horizontalHeader().sortIndicatorOrder() == Qt.SortOrder.DescendingOrder else Qt.SortOrder.DescendingOrder)

    def actualizar_datos(self):
        try:
            self.limpiar_tabla()
            self.establecer_conexion_base_de_datos()
            self.acceder_base_de_datos()
            self.mostrar_clicked()
        except Exception as e:
            print(f"Error al actualizar datos: {e}")
        finally:
            self.cerrar_conexion_base_de_datos()

    def primera_vez(self):
        if self.primer_mostrado:
            self.ajustar_tamanio()
            self.primer_mostrado = False

def main():
    app = QApplication(sys.argv)
    window = exportN()
    window.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
