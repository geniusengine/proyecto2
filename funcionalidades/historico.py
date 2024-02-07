
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
Dernière modification : mercredi 7 février 2024 à 17:12:18"""

import os
import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QTableWidget, \
    QTableWidgetItem, QHeaderView, QHBoxLayout , QLabel, QDateTimeEdit, QFileDialog, QMessageBox
from PyQt6.QtGui import QIcon, QColor
from PyQt6.QtCore import QTimer, Qt, QDateTime
import pymssql
import pandas as pd
from datetime import datetime

class Histo(QMainWindow):
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

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.actualizar_datos)
        self.timer.start(240000)  
        
        self.txt_filtro_fecha_inicio = QDateTimeEdit(self)
        self.txt_filtro_fecha_fin = QDateTimeEdit(self)
        self.btn_aplicar_filtro = QPushButton("Aplicar Filtro", self)
        self.btn_aplicar_filtro.clicked.connect(self.aplicar_filtro)

        filtro_layout = QHBoxLayout()
        filtro_layout.addWidget(QLabel("Fecha de inicio:"))
        filtro_layout.addWidget(self.txt_filtro_fecha_inicio)
        filtro_layout.addWidget(QLabel("Fecha de fin:"))
        filtro_layout.addWidget(self.txt_filtro_fecha_fin)
        filtro_layout.addWidget(self.btn_aplicar_filtro)

        self.layout_vertical.addLayout(filtro_layout)

        self.crear_botones()

        self.layout_vertical.addWidget(self.btn_exportar)
        self.layout_vertical.addLayout(self.layout_horizontal)

        self.table = QTableWidget()
        self.table.setStyleSheet(
            "QTableView { gridline-color: white; }"
            "QTableCornerButton::section { background-color: #d3d3d3; border: 1px solid black; }"
            "QHeaderView::section { background-color: #d3d3d3; border: 1px solid black; }"
        )
        self.layout_vertical.addWidget(self.table)
        self.table.horizontalHeader().sectionClicked.connect(self.ordenar_tabla)
        self.central_widget.setLayout(self.layout_vertical)
        self.ajustar_tamanio()

        self.establecer_conexion_base_de_datos()
        self.acceder_base_de_datos()
        self.mostrar_clicked()
        self.cerrar_conexion_base_de_datos()

        self.setGeometry(100, 100, 400, 300)

    def crear_botones(self):
        self.btn_exportar = self.crear_boton('Exportar', self.exportar_clicked)

    def aplicar_filtro(self):
        fecha_inicio = self.txt_filtro_fecha_inicio.dateTime().toPyDateTime()
        fecha_fin = self.txt_filtro_fecha_fin.dateTime().toPyDateTime()

        self.limpiar_tabla()
        self.establecer_conexion_base_de_datos()
        self.acceder_base_de_datos(fecha_inicio, fecha_fin)
        self.mostrar_clicked()
        self.cerrar_conexion_base_de_datos()

    def crear_boton(self, texto, funcion):
        boton = QPushButton(texto, self)
        boton.clicked.connect(funcion)
        return boton

    def update_dashboard(self):
        self.label.setText("¡Panel Actualizado!")

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

    def eliminar_y_respaldo(self):
        try:
            self.establecer_conexion_base_de_datos()
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

    def acceder_base_de_datos(self, fecha_inicio=None, fecha_fin=None): 
        try:
            with self.db_connection.cursor() as cursor:
                query = "SELECT fechaNotificacion, numjui, nombTribunal, demandante, demandado, repre, mandante, domicilio, comuna, encargo, soli, arancel, estadoNoti, estadoCausa FROM buscar_historico"
                
                if fecha_inicio and fecha_fin:
                    query += " WHERE fechaNotificacion BETWEEN %s AND %s"
                    cursor.execute(query, (fecha_inicio, fecha_fin))
                else:
                    cursor.execute(query)

                resultados = cursor.fetchall()

            self.causas = []
            for fila in resultados:
                if len(fila) > 0:
                    fecha_formateada = fila[0].strftime("%d-%m-%Y")
                else:
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
                self.causas.append(causa)
        except pymssql.Error as db_error:
            print(f"Error al ejecutar la consulta SQL: {db_error}")
            self.db_connection.rollback()    
        except Exception as e:
            print(f"Error al acceder a la base de datos: {e}")

    def limpiar_tabla(self):
        self.table.clearContents()
        self.table.setRowCount(0)

    def obtener_fecha_actual(self):
        fecha_actual = QDateTime.currentDateTime()
        formato_fecha = fecha_actual.toString('yyyy-MM-dd HH:mm:ss')
        return formato_fecha

    def mostrar_clicked(self):
        self.table.setColumnCount(12)
        self.table.setHorizontalHeaderLabels(['Fecha notificacion',  'Rol', 'Tribunal', 'Demandante', 'Demandando', 'Representante', 'Mandante', 'Domicilio', 'Comuna', 'Encargo', 'Resultado', 'Arancel'])
        for row_index, causa in enumerate(self.causas):
            self.table.insertRow(row_index)
            notificada = causa["Notificada"]
            estampada = causa["estadoCausa"]
            for col_index, (key, value) in enumerate(causa.items()):
                if key == "Notificar":
                    button = self.crear_boton_con_icono("static/notificar.png", self.notificar_clicked)
                    self.table.setCellWidget(row_index, col_index, button)
                else:
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
                columnas_deseadas = ['Fecha notificacion',  'Rol', 'Tribunal', 'demandante',  'demandado', 'repre', 'Domicilio', 'Comuna', 'Encargo', 'Resultado', 'Arancel']
                df_seleccionado = df.loc[:, columnas_deseadas]
                ruta_archivo = os.path.join(selected_folder, f'Nomina {años}.xlsx')
                df_seleccionado.to_excel(ruta_archivo, index=False)
                QMessageBox.information(self, "Información", "Los datos se han exportado correctamente.")
            except Exception as e:
                QMessageBox.warning(self, "Advertencia", f"Error al exportar a Excel: {e}")

    def ordenar_tabla(self, logicalIndex):
        self.table.sortItems(logicalIndex, Qt.SortOrder.AscendingOrder if self.table.horizontalHeader().sortIndicatorOrder() == Qt.SortOrder.DescendingOrder else Qt.SortOrder.DescendingOrder)

    def notificar_clicked(self):
        button = self.sender()
        index = self.table.indexAt(button.pos())
        row, col = index.row(), index.column()
        causa = self.causas[row]
        
        selected_row = self.table.currentRow()

        if causa["Notificada"] == 1:
            QMessageBox.warning(self, "Advertencia", "Esta causa ya ha sido notificada.")
            return
        
        causa["Notificada"] = 1

        numjui_notificado = self.table.item(selected_row, 1).text()
        
        try:
            self.establecer_conexion_base_de_datos()
            with self.db_connection.cursor() as cursor:
                query = "UPDATE notificacion SET estadoNoti = 1 WHERE numjui = %s"
                cursor.execute(query, (causa['Rol'],))
            self.db_connection.commit()
        except pymssql.Error as db_error:
            print(f"Error al ejecutar la consulta SQL: {db_error}")
            self.db_connection.rollback()
            raise
        except Exception as e:
            print(f"Error desconocido: {e}")
            raise
        finally:
            self.cerrar_conexion_base_de_datos()

        self.table.cellWidget(row, col).setText("Si")
        self.actualizar_color_fila(row)
        QMessageBox.information(self, "Éxito", "Causa notificada correctamente.")

    def ajustar_tamanio(self):
        self.table.resizeColumnsToContents()
        total_width = sum(self.table.columnWidth(col) for col in range(self.table.columnCount()))
        min_width = max(self.width(), total_width)-70
        self.setMinimumWidth(min_width)
        self.adjustSize()
        
    def actualizar_color_fila(self, row):
        causa = self.causas[row]
        notificada = causa["Notificada"]
        estampada = causa["estadoCausa"]
        
        for col_index in range(self.table.columnCount()):
            item = self.table.item(row, col_index)
            if item is not None:
                self.color_y_etiqueta_celda(item, notificada, estampada)

        self.table.viewport().update()

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
    window = Histo()
    window.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()