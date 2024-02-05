"""
 _______       _            _     _          ______        _                 _ 
(_______)     (_)       _  (_)   | |        (____  \      (_)               | |
 _______  ____ _  ___ _| |_ _  __| |_____    ____)  ) ____ _ _____ ____   __| |
|  ___  |/ ___) |/___|_   _) |/ _  | ___ |  |  __  ( / ___) (____ |  _ \ / _  |
| |   | | |   | |___ | | |_| ( (_| | ____|  | |__)  ) |   | / ___ | | | ( (_| |
|_|   |_|_|   |_(___/   \__)_|\____|_____)  |______/|_|   |_\_____|_| |_|\____|
    
Auteur: matit(matit.pro@gmail.com) 
miscocos.py(Ɔ) 2024
Description : Saisissez la description puis « Tab »
Créé le :  jeudi 1 février 2024 à 13:40:07 
Dernière modification : lundi 5 février 2024 à 12:44:02"""

import os
import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QTableWidget, \
    QTableWidgetItem, QHeaderView, QCheckBox, QHBoxLayout , QMessageBox, QLabel,QLineEdit, QFileDialog
from PyQt6.QtGui import QColor, QIcon
from PyQt6.QtCore import QDateTime, QTimer, Qt, pyqtSignal
import pymssql
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
        #verifica si es la primera vez que mostrara los datos
        self.primer_mostrado = True

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)
        self.layout_vertical = QVBoxLayout()  # Crea un layout vertical
        self.layout_horizontal = QHBoxLayout()  # Crea un layout horizontal

        #Crea un temporizador para actualizar los datos cada 4 minuto
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.actualizar_datos)
        self.timer.start(240000)  # 240000 milisegundos = 4 minutos
        
        # Dentro del método initUI() en tu clase DashboardApp
        self.txt_filtro_comuna = QLineEdit(self)
        self.txt_filtro_mandante = QLineEdit(self)
        self.btn_aplicar_filtro = QPushButton("Aplicar Filtro", self)
        self.btn_aplicar_filtro.clicked.connect(self.aplicar_filtro)

        # Crear un contenedor para los widgets de filtro
        filtro_layout = QHBoxLayout()
        filtro_layout.addWidget(QLabel("Filtrar por Comuna:"))
        filtro_layout.addWidget(self.txt_filtro_comuna)
        filtro_layout.addWidget(QLabel("Filtrar por Mandante:"))
        filtro_layout.addWidget(self.txt_filtro_mandante)
        filtro_layout.addWidget(self.btn_aplicar_filtro)

        self.layout_vertical.addLayout(filtro_layout)
        # Crea botones
        self.crear_botones()

        # Añade botones al layout horizontal y el layout horizontal al layout vertical
        
        self.layout_vertical.addWidget(self.btn_exportar)
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

        # Agrega la leyenda de colores al layout vertical existente
        self.layout_vertical.addLayout(color_legend_layout)

        # Crea un temporizador para realizar la eliminación y respaldo cada 10 minutos
        self.timer_eliminar_respaldo = QTimer(self)

        self.timer_eliminar_respaldo.timeout.connect(self.eliminar_y_respaldo)
        self.timer_eliminar_respaldo.start(1800000)  # 600000 milisegundos = 10 minutos

    # crea los botones de la interfaz
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
                query = "SELECT fechaNotificacion, numjui, nombTribunal, demandante, demandado, repre, mandante, domicilio, comuna, encargo, soli, arancel, estadoNoti, estadoCausa FROM notificacion"
                
            
                # Aplicar filtros si se proporcionan
                if filtro_comuna:
                    query += f" WHERE comuna = '{filtro_comuna}'"
                if filtro_mandante:
                    query += f" AND mandante = '{filtro_mandante}'" if filtro_comuna else f" WHERE mandante = '{filtro_mandante}'"
                cursor.execute(query)
                resultados = cursor.fetchall()

            query += "AND  estadoNoti IS NULL" 
              
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
                        "Arancel": fila[11],
                        "Notificada": fila[12],
                        "estadoCausa": fila[13],
                }
                print(causa)
                self.causas.append(causa)
            self.cerrar_conexion_base_de_datos()
        except pymssql.Error as db_error:
            print(f"Error al ejecutar la consulta SQL: {db_error}")
            self.db_connection.rollback()    
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
        self.table.setColumnCount(12)
        self.table.setHorizontalHeaderLabels(['Fecha notificacion',  'Rol', 'Tribunal', 'demandante', 'Nombre demandando', 'Representante', 'Mandante', 'Domicilio', 'Comuna', 'Encargo', 'Resultado', 'Arancel'])
        for row_index, causa in enumerate(self.causas):
            self.table.insertRow(row_index)
            notificada = causa["Notificada"]
            estampada = causa["estadoCausa"]
            for col_index, (key, value) in enumerate(causa.items()):
                if key == "Notificar":
                    button = self.crear_boton_con_icono("static/notificar.png", self.notificar_clicked)
                    self.table.setCellWidget(row_index, col_index, button)
                else:
                    # Crea un objeto QTableWidgetItem para las otras columnas
                    item = QTableWidgetItem(str(value))
                    self.table.setItem(row_index, col_index, item)
                    self.color_y_etiqueta_celda(self.table.item(row_index, col_index), estampada, notificada)
        self.primera_vez()

    def exportar_clicked(self):
        # Abre un diálogo de selección de directorios
        selected_folder = QFileDialog.getExistingDirectory(self, "Selecciona la carpeta para guardar el archivo")

        # Si el usuario selecciona una carpeta, procede a exportar
        if selected_folder:
            now = datetime.now()
            años = now.strftime("%d-%m-%y")
            horas = now.strftime("%H:%M")

            try:
                df = pd.DataFrame(self.causas)
                columnas_deseadas = ['Fecha notificacion',  'Rol', 'Tribunal', 'demandante',  'demandado', 'repre', 'Encargo', 'Domicilio', 'Comuna', 'Encargo', 'Resultado', 'Arancel']
                df_seleccionado = df.loc[:, columnas_deseadas]
                
                # Combina la ruta de la carpeta seleccionada con el nombre del archivo
                ruta_archivo = os.path.join(selected_folder, f'Nomina.xlsx')
                
                df_seleccionado.to_excel(ruta_archivo, index=False)
                QMessageBox.information(self, "Información", "Los datos se han exportado correctamente.")
            except Exception as e:
                QMessageBox.warning(self, "Advertencia", f"Error al exportar a Excel: {e}")

# Función para ordenar la tabla según la columna clicada
    def ordenar_tabla(self, logicalIndex):
        self.table.sortItems(logicalIndex, Qt.SortOrder.AscendingOrder if self.table.horizontalHeader().sortIndicatorOrder() == Qt.SortOrder.DescendingOrder else Qt.SortOrder.DescendingOrder)

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
    window = exportN()

    window.show()
    sys.exit(app.exec())
    
# Ejecuta la función principal
if __name__ == '__main__':
    main()