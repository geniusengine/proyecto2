import sys
from passlib.hash import bcrypt
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QPushButton, QVBoxLayout, QWidget, QMessageBox
from PyQt6.QtSql import QSqlDatabase, QSqlQuery
from PyQt6.QtCore import QTimer
from PyQt6.QtGui import QIcon
import pymssql
import logging
from dashboard import DashboardApp

# Configurar el sistema de registro
logging.basicConfig(filename='registro.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class LoginApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.init_ui()
        self.init_db()

    def init_ui(self):
        self.setWindowTitle("Inicio de Sesión")
        self.setWindowIcon(QIcon("static/icons/icono-ventana.png"))
        self.setGeometry(100, 100, 300, 200)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
         # Desactiva la redimensión de la ventana 
        self.setFixedSize(300, 200)
        self.layout = QVBoxLayout()

        self.username_label = QLabel("Usuario:")
        self.username_input = QLineEdit()
        self.password_label = QLabel("Contraseña:")
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.login_button = QPushButton("Iniciar Sesión")
        self.login_button.clicked.connect(self.authenticate)

        self.layout.addWidget(self.username_label)
        self.layout.addWidget(self.username_input)
        self.layout.addWidget(self.password_label)
        self.layout.addWidget(self.password_input)
        self.layout.addWidget(self.login_button)

        self.central_widget.setLayout(self.layout)

    def init_db(self):
        self.db = pymssql.connect(
                server='vps-3697915-x.dattaweb.com',
                user='daniel',
                password='LOLxdsas--',
                database='micau5a'
            )

        if not self.db:
            print("Error al conectar a la base de datos MySQL.")
            sys.exit(1)

        self.cursor = self.db.cursor()

    def authenticate(self):
        username = self.username_input.text()
        password = self.password_input.text()

        # Consultar la base de datos MySQL para verificar las credenciales
        sql = "SELECT password FROM usuarios WHERE username = %s"
        values = (username,)

        self.cursor.execute(sql, values)
        result = self.cursor.fetchone()

        if result:
            stored_password = result[0]
            if bcrypt.verify(password, stored_password):
                # Inicio de sesión exitoso
                QMessageBox.information(self, "Inicio de Sesión", "Inicio de sesión exitoso.")

                # Cerrar la ventana de inicio de sesión
                self.close()

                # Agregar información al registro
                logging.info(f'Inicio de sesión exitoso para el usuario: {username}')

                # Abrir la ventana del dashboard
                self.dashboard_window = DashboardApp()
                self.dashboard_window.show()

            else:
                # Contraseña incorrecta
                QMessageBox.warning(self, "Inicio de Sesión", "Contraseña incorrecta.")
                logging.warning(f'Inicio de sesión fallido')
        else:
            # Usuario no encontrado
            QMessageBox.warning(self, "Inicio de Sesión", "Usuario no encontrado.")
            logging.warning(f'Inicio de secion erroneo')

    def close_db_connection(self):
        self.cursor.close()
        self.db.close()

def main():
    app = QApplication(sys.argv)
    login_app = LoginApp()
    login_app.show()

    # Cierra la conexión de la base de datos cuando se cierra la aplicación
    app.aboutToQuit.connect(login_app.close_db_connection)

    sys.exit(app.exec())

if __name__ == '__main__':
    main()