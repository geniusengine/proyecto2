import sys
from passlib.hash import bcrypt
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QPushButton, QVBoxLayout, QWidget, QMessageBox
from PyQt6.QtSql import QSqlDatabase, QSqlQuery
from PyQt6.QtCore import QTimer
import pymssql
from dashboard import Dashboard

class LoginApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.init_ui()
        self.init_db()

    def init_ui(self):
        self.setWindowTitle("Inicio de Sesión")
        self.setGeometry(100, 100, 300, 200)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

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

                # Abrir la ventana del dashboard
                #self.dashboard_window = Dashboard()
                #self.dashboard_window.show()
            else:
                # Contraseña incorrecta
                QMessageBox.warning(self, "Inicio de Sesión", "Contraseña incorrecta.")
        else:
            # Usuario no encontrado
            QMessageBox.warning(self, "Inicio de Sesión", "Usuario no encontrado.")

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