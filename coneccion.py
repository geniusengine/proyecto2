"""
 _______       _            _     _          ______        _                 _ 
(_______)     (_)       _  (_)   | |        (____  \      (_)               | |
 _______  ____ _  ___ _| |_ _  __| |_____    ____)  ) ____ _ _____ ____   __| |
|  ___  |/ ___) |/___|_   _) |/ _  | ___ |  |  __  ( / ___) (____ |  _ \ / _  |
| |   | | |   | |___ | | |_| ( (_| | ____|  | |__)  ) |   | / ___ | | | ( (_| |
|_|   |_|_|   |_(___/   \__)_|\____|_____)  |______/|_|   |_\_____|_| |_|\____|
    
Auteur: danie(danie.pro@gmail.com) 
coneccion.py(Ɔ) 2023
Description : Saisissez la description puis « Tab »
Créé le :  samedi 28 octobre 2023 à 14:40:33 
Dernière modification : samedi 28 octobre 2023 à 18:06:12
"""
import sys
import pyodbc
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget

class DatabaseApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

        # Realiza la conexión a la base de datos en el constructor
        self.connect_to_database()

    def initUI(self):
        self.setWindowTitle('Aplicación de Base de Datos SQL Server')
        self.setGeometry(100, 100, 400, 200)

        layout = QVBoxLayout()

        self.status_label = QLabel('', self)
        layout.addWidget(self.status_label)

        central_widget = QWidget(self)
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def connect_to_database(self):
        try:
            # Configura la cadena de conexión a tu base de datos SQL Server en la nube
            conn_str = (
                r'DRIVER={ODBC Driver 18 for SQL Server};'
                r'SERVER=vps-3697915-x.dattaweb.com;'
                r'DATABASE= micau5a;'
                r'UID=daniel;'
                r'PWD=LOLxdsas--;'
                r'Encrypt=yes;'
                r'TrustServerCertificate=yes;'
                r'Connection Timeout=10;'
            )
            connection = pyodbc.connect(conn_str)
            
            self.status_label.setText('Conexión exitosa a la base de datos en la nube (SQL Server).')
            # Aquí puedes realizar operaciones en la base de datos según tus necesidades
        except pyodbc.Error as e:
            self.status_label.setText(f'Error de conexión a la base de datos en la nube: {str(e)}')

def main():
    app = QApplication(sys.argv)
    window = DatabaseApp()
    window.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
