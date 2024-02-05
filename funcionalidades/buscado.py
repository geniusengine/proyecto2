import pymssql
import subprocess  # Importa el módulo subprocess
import sys
from PyQt6.QtGui import QColor, QIcon
from PyQt6.QtWidgets import QMessageBox,QApplication,QRadioButton, QButtonGroup, QMainWindow, QPushButton, QLabel, QLineEdit,QTableWidgetItem ,QVBoxLayout, QHBoxLayout, QWidget, QCheckBox, QListWidget, QListWidgetItem,QTableWidget
from PyQt6.QtCore import Qt
from funcionalidades import estampado_app
import pymssql
import logging

# Configurar el sistema de registro
logging.basicConfig(filename='registro.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class BuscadorDatosCausaApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Buscador de Datos de Causa")
        self.setWindowIcon(QIcon("static/icono-ventana.png"))
        self.setGeometry(100, 100, 600, 400)

        self.initUI()

    def initUI(self):
        main_layout = QVBoxLayout()

        # Parte superior (en una sola fila)
        search_layout = QHBoxLayout()


        self.check_numjui = QCheckBox("Rol")
        self.numjui_input = QLineEdit(self)

        self.check_tribunal = QCheckBox("Tribunal")
        self.tribunal_input = QLineEdit(self)

        search_layout.addWidget(self.check_numjui)
        search_layout.addWidget(self.numjui_input)

        search_layout.addWidget(self.check_tribunal)
        search_layout.addWidget(self.tribunal_input)

        self.button_search = QPushButton("Buscar", self)
        self.button_search.clicked.connect(self.search_data)
        search_layout.addWidget(self.button_search)

        main_layout.addLayout(search_layout)

        # Parte inferior (resultados con casillas de verificación y botones)
        # self.result_list = QListWidget(self)
        # main_layout.addWidget(self.result_list)
        
        #crea tabla que mostrara resultados de buscar
        self.table = QTableWidget()
        main_layout.addWidget(self.table)
        # Grupo de exclusión para los checkboxes
        self.checkbox_group = QButtonGroup()
        self.checkbox_group.setExclusive(True)#solo se puede seleccionar un checkbox a la vez
        self.checkbox_group.buttonToggled.connect(self.checkbox_seleccionado)
        # Inicializa causa_seleccionada como una lista vacía
        self.causa_seleccionada = []
        self.result_checkboxes = []

        self.buttons_layout = QHBoxLayout()
        self.button_select = QPushButton("Seleccionar", self)
        self.button_select.clicked.connect(self.select_results)
        self.buttons_layout.addWidget(self.button_select)

        self.button_clear = QPushButton("Limpiar", self)
        self.button_clear.clicked.connect(self.limpiar_tabla)
        self.buttons_layout.addWidget(self.button_clear)

        main_layout.addLayout(self.buttons_layout)

        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

    # limpia la tabla
    def limpiar_tabla(self):
        self.table.clearContents()
        self.table.setRowCount(0)

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

#busca los datos en la base de datos en base al rol o tribunal
    def search_data(self):
        search_by_numjui = self.check_numjui.isChecked()
        search_by_tribunal = self.check_tribunal.isChecked()
        numjui = self.numjui_input.text()
        tribunal = self.tribunal_input.text()

        if not search_by_numjui and not search_by_tribunal:
            print("No se ha seleccionado ningún criterio de búsqueda.")
            return
        try:
            connection = pymssql.connect(
                server='vps-3697915-x.dattaweb.com',
                user='daniel',
                password='LOLxdsas--',
                database='micau5a'
            )
            cursor = connection.cursor()
            if search_by_numjui:#si se selecciono numjui para buscar se ejecuta esta query
                query = """
                SELECT fechaNotificacion, numjui, nombTribunal
                FROM buscar_historico
                WHERE numjui = %s
                """
                cursor.execute(query, (numjui))
            elif search_by_tribunal:#si se selecciono tribunal para buscar se ejecuta esta query
                query = """
                SELECT fechaNotificacion, numjui, nombTribunal
                FROM buscar_historico
                WHERE nombtribunal = %s
                """
                cursor.execute(query, (tribunal))
            elif search_by_numjui and search_by_tribunal:#si se selecciono ambos para buscar se ejecuta esta query
                query = """
                SELECT fechaNotificacion, numjui, nombTribunal
                FROM buscar_historico
                WHERE numjui = %s OR nombtribunal = %s
                """
                cursor.execute(query, (numjui,tribunal))
            resultado = cursor.fetchall()
            connection.close()
            self.limpiar_tabla()
            if resultado:#si hay datos en la base de datos los muestra en la lista
                self.table.setStyleSheet(
                "QTableView { gridline-color: grey; }"
                "QTableCornerButton::section { background-color: #d3d3d3; border: 1px solid black; }"
                "QHeaderView::section { background-color: #d3d3d3; border: 1px solid black; }"
                "QTableWidget::item {padding: 5px;text-align: center;}"
                )
                self.causas = []
                for fila in resultado:
                    fecha_formateada = fila[0].strftime("%d-%m-%Y")
                    causa={
                        "fecha Notificacion": fecha_formateada,
                        "rol": fila[1],
                        "tribunal": fila[2],
                        "checkbox": "",
                    }
                    self.causas.append(causa)
                self.table.setColumnCount(4)
                self.table.setHorizontalHeaderLabels(['Fecha',  'Rol', 'Tribunal','Seleccionar'])
                for row_index, causa in enumerate(self.causas):
                    self.table.insertRow(row_index)
                    for column_index, (key,value) in enumerate(causa.items()):
                        if key == "checkbox":
                            checkbox = QRadioButton()
                            self.checkbox_group.addButton(checkbox)
                            self.table.setCellWidget(row_index, column_index, checkbox)
                        item = QTableWidgetItem(str(value))  
                        self.table.setItem(row_index, column_index, item)
                        #logging.info(f'Busqueda de causa {self.numjui}-{self.nombTribunal}')

                            
            else:#si no hay datos en la base de datos muestra un mensaje
                self.limpiar_tabla()
                self.table.setStyleSheet("")
                self.table.setColumnCount(1)         
                self.table.setHorizontalHeaderLabels(['No se encontraron datos para la búsqueda especificada.'])
                print("no hay datos")
        except pymssql.Error as err:     
            print(" hola" ,err)
            self.limpiar_tabla()
            self.table.setColumnCount(1)
            self.table.setStyleSheet("")
            self.table.setHorizontalHeaderLabels([str(err)])                                                                                                                                        

        self.ajustar_tamanio()
    def ajustar_tamanio(self):
        self.table.resizeColumnsToContents()
        total_width = sum(self.table.columnWidth(col) for col in range(self.table.columnCount()))
        min_width = max(self.width(), total_width)
        self.setMinimumWidth(min_width+40)
        self.adjustSize()

    def checkbox_seleccionado(self, checkbox, checked):
        if checked:
            # Obtener la fila y las columnas seleccionadas
            row_index = self.table.indexAt(checkbox.pos()).row()
            cols = self.table.columnCount()
            # Obtener los valores de las celdas de la fila
            self.causa_seleccionada = [self.table.item(row_index, col).text() for col in range(cols)]
            # Imprimir o hacer algo con los valores
            
#muestra los datos relacionados con la busqueda en la base de datos y los muestra en la tabla
    def select_results(self):
        self.limpiar_tabla()
        self.table.setColumnCount(15)
        self.table.setHorizontalHeaderLabels(['Fecha',  'Rol', 'Tribunal', 'Nombre demandante',  'Nombre demandando', 'Representante', 'Nombre mandante', 'Domicilio', 'Comuna', 'Encargo', 'Solicitud', 'Arancel','Actuacion',
                                            'Notificar','Estampar'])
        try:
            if self.causa_seleccionada :#si se selecciono una causa para buscar se ejecuta esta query
                try:
                    connection = pymssql.connect(
                        server='vps-3697915-x.dattaweb.com',
                        user='daniel',
                        password='LOLxdsas--',
                        database='micau5a'
                    )
                    numjui = self.causa_seleccionada[1]
                    nombTribunal = self.causa_seleccionada[2]

                    cursor = connection.cursor()
                    self.causas_seleccionadas = []

                    if numjui:#si se selecciono numjui para buscar se ejecuta esta query
                        query = """
                        SELECT fechaNotificacion, numjui, nombTribunal, nombdemandante,  demandado,repre, mandante , domicilio, comuna,encargo, soli, arancel, estadoNoti, estadoCausa,actu
                        FROM buscar_historico
                        WHERE numjui = %s
                        """
                        cursor.execute(query, (numjui))
                    elif nombTribunal:#si se selecciono tribunal para buscar se ejecuta esta query
                        query = """
                        SELECT fechaNotificacion, numjui, nombTribunal, nombdemandante,  demandado,repre, mandante , domicilio, comuna,encargo, soli, arancel, estadoNoti, estadoCausa,actu
                        FROM buscar_historico
                        WHERE nombtribunal = %s
                        """
                        cursor.execute(query, (nombTribunal))
                    elif numjui and nombTribunal:#si se selecciono ambos para buscar se ejecuta esta query
                        query = """
                        SELECT fechaNotificacion, numjui, nombTribunal, nombdemandante,  demandado,repre, mandante , domicilio, comuna,encargo, soli, arancel, estadoNoti, estadoCausa,actu
                        FROM buscar_historico
                        WHERE numjui = %s OR nombtribunal = %s
                        """
                    causas = cursor.fetchall()
                    #self.causas_seleccionadas.extend(causas)#agrega los datos a la lista
                    if causas:
                        
                        for fila in causas:
                            fecha_formateada = fila[0].strftime("%d-%m-%Y")
                            datos_causa = {
                                "Fecha notificacion": fecha_formateada,
                                "Rol": fila[1],
                                "Tribunal": fila[2],
                                "Nombre demandante": fila[3],
                                "Nombre demandado": fila[4],
                                "repre": fila[5],
                                "mandante": fila[6],
                                "Domicilio": fila[7],
                                "Comuna": fila[8],
                                "Encargo": fila[9],
                                "Solicitud": fila[10],
                                "Arancel": fila[11],
                                "actu": fila [12],
                                "Notificar": "Notificar",
                                "Estampada": "Estampada",
                                "Notificada": fila[13],
                                "estadoCausa": fila[14],
                            }
                            self.causas_seleccionadas.append(datos_causa)
                        self.mostrar_datos_causa()
                    else:
                        self.limpiar_tabla()
                        self.table.setStyleSheet("")
                        self.table.setColumnCount(1)         
                        self.table.setHorizontalHeaderLabels(['No se encontraron datos para la búsqueda especificada.'])
                except pymssql.Error as err:
                    self.limpiar_tabla()
                    self.table.setStyleSheet("")
                    self.table.setColumnCount(1)         
                    self.table.setHorizontalHeaderLabels(['No se Ha seleccionado nada aún para buscar.'])
                    print(err)  
            else:
                self.limpiar_tabla()
                self.table.setStyleSheet("")
                self.table.setColumnCount(1)         
                self.table.setHorizontalHeaderLabels(['Ningún resultado seleccionado'])
            
        except pymssql.Error as err:
            self.limpiar_tabla()
            self.table.setStyleSheet("")
            self.table.setColumnCount(1)         
            self.table.setHorizontalHeaderLabels(['No se encontraron datos para la búsqueda especificada.'])
            print(err)  


        self.ajustar_tamanio()

    #muestra los datos encontrados segun la causa seleccionada
    def mostrar_datos_causa(self):
        self.limpiar_tabla()
        for row_index, causa in enumerate(self.causas_seleccionadas):# row_index es el indice de la fila y causa es el diccionario con los datos de la causa
            self.table.insertRow(row_index)
            print(causa)    
            if 'Notificada' in causa and 'estadoCausa' in causa:  # Verifica si las claves existen en el diccionario
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
            else:
                print("Las claves 'Notificada' y 'estadoCausa' no existen en el diccionario.")
        self.ajustar_tamanio()

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
    
    # al notificar cambia el estado de la causa
    def notificar_clicked(self):
        button = self.sender()
        index = self.table.indexAt(button.pos())
        row, col = index.row(), index.column()
        causa = self.causas_seleccionadas[row]

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
                query = f"UPDATE AUD_notificacion SET estadoNoti = 1"
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
        self.table.cellWidget(row, col).setText("Si")
        self.actualizar_color_fila(row)
        # Proporciona un mensaje de éxito al usuario
        QMessageBox.information(self, "Éxito", "Causa notificada correctamente.")

        logging.info(f'Se notifico causa: {numjui_notificado}')

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
            demandado = self.table.item(selected_row, 4).text()
            repre = self.table.item(selected_row, 5).text()
            mandante = self.table.item(selected_row, 6).text()
            domicilio = self.table.item(selected_row, 7).text()
            comuna = self.table.item(selected_row, 8).text()
            encargo = self.table.item(selected_row, 9).text()
            soli = self.table.item(selected_row, 10).text()
            arancel = self.table.item(selected_row, 11).text()
            
            # Importa Estampadoxd localmente
            self.ex3 = estampado_app.Estampadoxd(fechaNotificacion, numjui, nombTribunal, nombdemandante,  demandado, repre, mandante, domicilio, comuna, encargo, soli, arancel)
            self.ex3.show()
        
        button = self.sender()
        index = self.table.indexAt(button.pos())
        row, col = index.row(), index.column()
        causa = self.causas_seleccionadas[row]
        color = QColor(250, 193, 114)

        # Verifica si la causa ya ha sido notificada
        if causa["Estampada"] == 1:
            QMessageBox.warning(self, "Advertencia", "Esta causa ya ha sido notificada.")
            return
        
        # Actualiza la información localmente
        causa["Estampada"] = 1

        numjui = self.table.item(selected_row, 1).text()
        
        # Actualiza el valor en la base de datos
        try:
            self.establecer_conexion_base_de_datos()
            with self.db_connection.cursor() as cursor:
                query = f"UPDATE buscar_historico SET estadoCausa = 1"
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
        
        # Configurar el sistema de registro
        logging.info(f'Se estampo causa: {numjui}')

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
     # función para actualizar el color de la fila
    def actualizar_color_fila(self, row):
        causa = self.causas_seleccionadas[row]
        print(causa)
        notificada = causa["Notificada"]
        estampada = causa["estadoCausa"]
        
        for col_index in range(self.table.columnCount()):
            item = self.table.item(row, col_index)
            if item is not None:
                # Llamas a la función que establece el color para cada celda
                self.color_y_etiqueta_celda(item, notificada, estampada)

        # Actualiza la vista de la tabla
        self.table.viewport().update()
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = BuscadorDatosCausaApp()
    window.show()
    sys.exit(app.exec())
