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
Dernière modification : jeudi 1 février 2024 à 15:32:19"""

import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
import pandas as pd

class FiltroVentana(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Filtro de Exportación')
        self.setGeometry(300, 300, 400, 200)

        self.layout = QVBoxLayout()

        self.label_comuna = QLabel('Filtrar por Comuna:')
        self.txt_filtro_comuna = QLineEdit(self)
        self.label_mandante = QLabel('Filtrar por Mandante:')
        self.txt_filtro_mandante = QLineEdit(self)

        self.btn_aplicar_filtro = QPushButton("Aplicar Filtro", self)
        self.btn_aplicar_filtro.clicked.connect(self.aplicar_filtro)

        self.layout.addWidget(self.label_comuna)
        self.layout.addWidget(self.txt_filtro_comuna)
        self.layout.addWidget(self.label_mandante)
        self.layout.addWidget(self.txt_filtro_mandante)
        self.layout.addWidget(self.btn_aplicar_filtro)

        self.setLayout(self.layout)

    def aplicar_filtro(self):
        filtro_comuna = self.txt_filtro_comuna.text()
        filtro_mandante = self.txt_filtro_mandante.text()

        if not filtro_comuna or not filtro_mandante:
            QMessageBox.warning(self, "Advertencia", "Por favor, complete todos los campos de filtro.")
            return

        try:
            df = pd.DataFrame(self.causas)
            columnas_deseadas = ['fecha',  'Rol', 'Tribunal', 'Nombre demandante', 'Apellido demandante', 'Nombre demandando', 'Representante', 'Quien Encarga', 'Domicilio', 'Comuna', 'Encargo', 'Resultado', 'Arancel']
            df_filtrado = df[(df['Comuna'] == filtro_comuna) & (df['Quien Encarga'] == filtro_mandante)]
            df_seleccionado = df_filtrado.loc[:, columnas_deseadas]
            df_seleccionado.to_excel('as.xlsx', index=False)
            QMessageBox.information(self, "Información", "Los datos se han exportado correctamente.")
        except Exception as e:
            QMessageBox.warning(self, "Advertencia", f"Error al exportar a Excel: {e}")
            
            print(f"Error al exportar a Excel: {e}")


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
def main():
    app = QApplication(sys.argv)
    window = FiltroVentana()
    window.show()
    sys.exit(app.exec())

# Ejecuta la función principal
if __name__ == '__main__':
    main()