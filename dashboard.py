import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QTableWidget, QTableWidgetItem, QHeaderView, QCheckBox, QHBoxLayout , QMessageBox, QLabel,QLineEdit
from PyQt6.QtGui import QColor, QIcon
from PyQt6.QtCore import QDateTime, QTimer, Qt, pyqtSignal
import pymssql
import pandas as pd
import logging
from funcionalidades.buscado import BuscadorDatosCausaApp
from funcionalidades.insertar_excel import ExcelToDatabaseApp
from funcionalidades.insertar_manual import MiApp
from funcionalidades.estampado_app import Estampadoxd
from funcionalidades.dashboard_historial_actuaciones import DashboardHistorialActuaciones
from funcionalidades.exportar import exportN
from funcionalidades.historico import Histo

# Configurar el sistema de registro
logging.basicConfig(filename='registro.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class DashboardApp(QMainWindow):
    datos_actualizados_signal = pyqtSignal()
    def __init__(self):
        super().__init__()
        self.db_connection = None
        self.initUI()
    
    def initUI(self):
        self.setWindowTitle('Dashboard App')
        self.setWindowIcon(QIcon("static/icono-ventana.png"))
        self.setGeometry(100, 100, 1280, 720)
        #verifica si es la primera vez que mostrara los datos
        self.primer_mostrado = True

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)
        self.layout_vertical = QVBoxLayout()  # Crea un layout vertical
        self.layout_horizontal = QHBoxLayout()  # Crea un layout horizontal

        #Crea un temporizador para actualizar los datos cada 4 minuto
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.actualizar_datos)
        self.timer.start(15000)  # 240000 milisegundos = 4 minutos
        
        # Añadir el contenedor de filtro al diseño vertical
        # self.layout_vertical.addLayout(filtro_layout)
        # Crea botones
        self.crear_botones()

        # Añade botones al layout horizontal y el layout horizontal al layout vertical
        self.layout_horizontal.addWidget(self.btn_buscar)
        self.layout_horizontal.addWidget(self.btn_Insertar_manual)
        self.layout_horizontal.addWidget(self.btn_historial_actuaciones)
        self.layout_horizontal.addWidget(self.btn_exportar)
        self.layout_horizontal.addWidget(self.btn_historico)
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
        self.ajustar_tamanio()

        # Llama automáticamente a acceder_base_de_datos y mostrar_clicked al iniciar la aplicación
        self.establecer_conexion_base_de_datos()
        self.acceder_base_de_datos()
        self.mostrar_clicked()

        self.setGeometry(100, 100, 400, 300)

        # Agrega un contenedor para la leyenda de colores
        color_legend_layout = QHBoxLayout()

        # Círculo verde con texto
        green_widget = QWidget()
        green_layout = QHBoxLayout()
        green_label = QLabel()
        green_label.setFixedSize(20, 20)
        green_label.setStyleSheet("background-color: rgb(46, 204, 113); border-radius: 10px;")
        green_text = QLabel("Estampada y Notificada")
        green_text.setStyleSheet("color: rgb(46, 204, 113)")
        green_layout.addWidget(green_label)
        green_layout.addWidget(green_text)
        green_widget.setLayout(green_layout)
        color_legend_layout.addWidget(green_widget)

        # Círculo amarillo con texto
        yellow_widget = QWidget()
        yellow_layout = QHBoxLayout()
        yellow_label = QLabel()
        yellow_label.setFixedSize(20, 20)
        yellow_label.setStyleSheet("background-color: rgb(250, 193, 114); border-radius: 10px;")
        yellow_text = QLabel("No estampada y Notificada")
        yellow_text.setStyleSheet("color: rgb(250, 193, 114);")
        yellow_layout.addWidget(yellow_label)
        yellow_layout.addWidget(yellow_text)
        yellow_widget.setLayout(yellow_layout)
        color_legend_layout.addWidget(yellow_widget)

        # Círculo rojo con texto
        red_widget = QWidget()
        red_layout = QHBoxLayout()
        red_label = QLabel()
        red_label.setFixedSize(20, 20)
        red_label.setStyleSheet("background-color: rgb(224, 92, 69); border-radius: 10px;")
        red_text = QLabel("No Estampada y No Notificada")
        red_text.setStyleSheet("color: rgb(224, 92, 69);")
        red_layout.addWidget(red_label)
        red_layout.addWidget(red_text)
        red_widget.setLayout(red_layout)
        color_legend_layout.addWidget(red_widget)

        # Agrega la leyenda de colores al layout vertical existente
        self.layout_vertical.addLayout(color_legend_layout)

        # Crea un temporizador para realizar la eliminación y respaldo cada 10 minutos
        self.timer_eliminar_respaldo = QTimer(self)

        self.timer_eliminar_respaldo.timeout.connect(self.eliminar_y_respaldo)
        self.timer_eliminar_respaldo.start(15000)  # 600000 milisegundos = 10 minutos



    # crea los botones de la interfaz
    def crear_botones(self):
        self.btn_buscar = self.crear_boton('Buscar', self.buscar_clicked)
        self.btn_Insertar_manual = self.crear_boton('Insertar Manual', self.Insertar_manual_clicked)
        self.btn_historial_actuaciones = self.crear_boton('Historial Actuaciones', self.historial_actuaciones_clicked)
        self.btn_exportar = self.crear_boton('Exportar', self.exportar_clicked)
        self.btn_historico = self.crear_boton('Historico', self.historico_clicked)


    # crea cada boton que se necesite
    def crear_boton(self, texto, funcion):
        boton = QPushButton(texto, self)
        boton.clicked.connect(funcion)
        return boton
    # crea un boton con un icono
    def crear_boton_con_icono(self, icono_path, funcion):
        boton = QPushButton(self)
        icono = QIcon()
        boton.setIcon(icono)
        boton.clicked.connect(funcion)
        return boton
    
    def update_dashboard(self):
        # Esta función se llamará cuando se guarden los datos
        self.label.setText("¡Panel Actualizado!")
        
    
    def combo_box_changed(self, row, col, index):
        # Aquí deberías escribir el código que se ejecutará cuando cambie el índice del combo box
        pass

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


    def eliminar_y_respaldo(self):
        try:
            self.establecer_conexion_base_de_datos()

            # Elimina los datos de la tabla notificacion donde estadoNoti = 1
            with self.db_connection.cursor() as cursor:
                delete_query = "DELETE FROM notificacion WHERE estadoNoti = 1 and estadoCausa = 1"
                cursor.execute(delete_query)

            self.db_connection.commit()

        except pymssql.Error as db_error:
            print(f"Error al ejecutar la consulta SQL: {db_error}")
            self.db_connection.rollback()
        except Exception as e:
            print(f"Error desconocido: {e}")
        finally:
            self.cerrar_conexion_base_de_datos()

    # accede a la base de datos
    def acceder_base_de_datos(self, filtro_comuna=None, filtro_mandante=None):
        try:
            with self.db_connection.cursor() as cursor:
                query = "SELECT fechaNotificacion, numjui, nombTribunal, demandante, demandado, repre, mandante, domicilio, comuna, encargo, soli, arancel, estadoNoti, estadoCausa,actu FROM notificacion"
                
                # Aplicar filtros si se proporcionan
                if filtro_comuna:
                    query += f" WHERE comuna = '{filtro_comuna}'"
                if filtro_mandante:
                    query += f" AND mandante = '{filtro_mandante}'" if filtro_comuna else f" WHERE mandante = '{filtro_mandante}'"
                cursor.execute(query)
                resultados = cursor.fetchall()
           
            self.causas = []
            for fila in resultados:
                if len(fila) > 0:
                    fecha_formateada = fila[0].strftime("%d-%m-%Y")
                else:
                    # Manejar la situación donde la tupla está vacía
                    fecha_formateada = "Fecha no disponible"
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
                        "Arancel": 'Arancel',
                        "actu":fila[14],
                        "Notificar": "Notificar",
                        "Estampada": "Estampada",
                        "Notificada": fila[12],
                        "estadoCausa": fila[13],
                }
                
                self.causas.append(causa)
            self.cerrar_conexion_base_de_datos()
        except Exception as e:
            print(f"Error al acceder a la base de datos: {e}")
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


# muestra los datos en la tabla
    def mostrar_clicked(self):
        self.table.setColumnCount(15)
        self.table.setHorizontalHeaderLabels(['Fecha notificacion',  'Rol', 'Tribunal', 'demandante', 'Nombre demandando', 'Representante', 'Mandante', 'Domicilio', 'Comuna', 'Encargo', 'Resultado', 'Arancel','Actuacion',
                                            'Notificar','Estampar'])
        for row_index, causa in enumerate(self.causas):
            self.table.insertRow(row_index)
            notificada = causa["Notificada"]
            estampada = causa["estadoCausa"]
            for col_index, (key, value) in enumerate(causa.items()):
                if key == "Notificar":
                    button = self.crear_boton_con_icono("static/notificar.png", self.notificar_clicked)
                    self.table.setCellWidget(row_index, col_index, button)
                elif key == "Estampada":
                    button = self.crear_boton_con_icono("static/firmar.png", self.estampar_clicked)
                    self.table.setCellWidget(row_index, col_index, button)
                else:
                    # Crea un objeto QTableWidgetItem para las otras columnas
                    item = QTableWidgetItem(str(value))
                    self.table.setItem(row_index, col_index, item)
                    self.color_y_etiqueta_celda(self.table.item(row_index, col_index), estampada, notificada)
                    
        self.primera_vez()

    def historico_clicked(self):
        self.exchistorico = Histo()
        self.exchistorico.show()

    def historial_actuaciones_clicked(self):
        print("Historial de actuaciones")
        self.exchistorial = DashboardHistorialActuaciones()
        self.exchistorial.show()
    def exportar_clicked(self):
        self.filtro= exportN()
        self.filtro.show()

# abre la ventana de insertar manualmente
    def Insertar_manual_clicked(self):
        # Lógica para insertar manualmente
        self.exa = MiApp()
        self.exa.show()
# abre la ventana de estampado
    def estampar_clicked(self):
        # Obtener la fila seleccionada
        selected_row = self.table.currentRow()
        # Verificar si se seleccionó una fila
        if selected_row != -1:

            notificada = self.causas[selected_row]["Notificada"]

            if not notificada:
                QMessageBox.warning(self, "Advertencia", "La causa debe ser notificada primero antes de estampar.")
                return

            # Obtener datos de la fila seleccionada
            fechaNotificacion = self.table.item(selected_row, 0).text()
            numjui = self.table.item(selected_row, 1).text()
            nombTribunal = self.table.item(selected_row, 2).text()
            demandante = self.table.item(selected_row, 3).text()
            demandado = self.table.item(selected_row, 4).text()
            repre = self.table.item(selected_row, 5).text()
            mandante = self.table.item(selected_row, 6).text()
            domicilio = self.table.item(selected_row, 7).text()
            comuna = self.table.item(selected_row, 8).text()
            encargo = self.table.item(selected_row, 9).text()
            soli = self.table.item(selected_row, 10).text()
            arancel = self.table.item(selected_row, 11).text()
    
            # Importa Estampadoxd localmente
            self.ex3 = Estampadoxd(fechaNotificacion, numjui, nombTribunal, demandante, demandado, repre, mandante, domicilio, comuna, encargo, soli, arancel)
            self.ex3.show()
        
        button = self.sender()
        index = self.table.indexAt(button.pos())
        row, col = index.row(), index.column()
        causa = self.causas[row]
        color = QColor(250, 193, 114)

        # Verifica si la causa ya ha sido notificada
        if causa["Estampada"] == 1:
            QMessageBox.warning(self, "Advertencia", "Esta causa ya ha sido estampada.")
            return
        
        # Actualiza la información localmente
        causa["Estampada"] = 1

        numjui = self.table.item(selected_row, 1).text()
        
        # Actualiza el valor en la base de datos
        try:
            self.establecer_conexion_base_de_datos()
            with self.db_connection.cursor() as cursor:
                query = "UPDATE notificacion SET estadoCausa = 1 WHERE numjui = %s"
                cursor.execute(query, (causa['Rol'],))
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

        # Configurar el sistema de registro
        logging.info(f'Se estampo causa: {numjui}')


# Función para ordenar la tabla según la columna clicada
    def ordenar_tabla(self, logicalIndex):
        self.table.sortItems(logicalIndex, Qt.SortOrder.AscendingOrder if self.table.horizontalHeader().sortIndicatorOrder() == Qt.SortOrder.DescendingOrder else Qt.SortOrder.DescendingOrder)
# abre la ventana de buscar
    def buscar_clicked(self):
        # Lógica para buscar
        self.bas = BuscadorDatosCausaApp()
        self.bas.show()

# al notificar cambia el estado de la causa
    def notificar_clicked(self):
        button = self.sender()
        index = self.table.indexAt(button.pos())
        row, col = index.row(), index.column()
        causa = self.causas[row]
        
        selected_row = self.table.currentRow()

        # Verifica si la causa ya ha sido notificada
        if causa["Notificada"] == 1:
            QMessageBox.warning(self, "Advertencia", "Esta causa ya ha sido notificada.")
            return
        
        # Actualiza la información localmente
        causa["Notificada"] = 1

        numjui_notificado = self.table.item(selected_row, 1).text()
        
        # Actualiza el valor en la base de datos
        try:
            self.establecer_conexion_base_de_datos()
            with self.db_connection.cursor() as cursor:
                query = "UPDATE notificacion SET estadoNoti = 1 WHERE numjui = %s"
                cursor.execute(query, (causa['Rol'],))
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
        self.table.cellWidget(row, col).setText("Si")
        self.actualizar_color_fila(row)
        # Proporciona un mensaje de éxito al usuario
        QMessageBox.information(self, "Éxito", "Causa notificada correctamente.")

        logging.info(f'Se notifico causa: {numjui_notificado}')
   
# ajusta el tamaño de la tabla ajustandose al contenido
    def ajustar_tamanio(self):
        self.table.resizeColumnsToContents()
        total_width = sum(self.table.columnWidth(col) for col in range(self.table.columnCount()))
        min_width = max(self.width(), total_width)-70
        self.setMinimumWidth(min_width)
        self.adjustSize()
# actualiza el color de la fila        
    # función para actualizar el color de la fila
    def actualizar_color_fila(self, row):
        causa = self.causas[row]
        notificada = causa["Notificada"]
        estampada = causa["estadoCausa"]
        
        for col_index in range(self.table.columnCount()):
            item = self.table.item(row, col_index)
            if item is not None:
                # Llamas a la función que establece el color para cada celda
                self.color_y_etiqueta_celda(item, notificada, estampada)

        # Actualiza la vista de la tabla
        self.table.viewport().update()
#define el color de la las filas de la tabla
    def color_y_etiqueta_celda(self, item, notificada, estampada):
        if item is not None:
            color = QColor(250, 193, 114)
            if notificada and estampada:
                color = QColor(46, 204, 113)  #verde
            elif not notificada and estampada:
                color = QColor(250, 193, 114)  # Amarillo
            elif not notificada and not estampada:
                color = QColor(224, 92, 69)  #rojo
            item.setBackground(color)
# actualiza los datos de la tabla
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
# Función principal
def main():
    app = QApplication(sys.argv)
    window = DashboardApp()

  
    window.show()
    sys.exit(app.exec())
    
# Ejecuta la función principal
if __name__ == '__main__':
    main()
    
 