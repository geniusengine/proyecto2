"""
 _______       _            _     _          ______        _                 _ 
(_______)     (_)       _  (_)   | |        (____  \      (_)               | |
 _______  ____ _  ___ _| |_ _  __| |_____    ____)  ) ____ _ _____ ____   __| |
|  ___  |/ ___) |/___|_   _) |/ _  | ___ |  |  __  ( / ___) (____ |  _ \ / _  |
| |   | | |   | |___ | | |_| ( (_| | ____|  | |__)  ) |   | / ___ | | | ( (_| |
|_|   |_|_|   |_(___/   \__)_|\____|_____)  |______/|_|   |_\_____|_| |_|\____|
    
Auteur: danie(mitchel.dmch@gmail.com) 
registro.py(Ɔ) 2023
Description : Saisissez la description puis « Tab »
Créé le :  samedi 26 août 2023 à 18:37:13 
Dernière modification : mercredi 31 janvier 2024 à 11:22:15
"""
import sys
import mysql.connector
from passlib.hash import bcrypt
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QPushButton, QVBoxLayout, QWidget, QMessageBox
from PyQt6.QtGui import QIcon
from PyQt6.QtSql import QSqlDatabase, QSqlQuery


class RegisterApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.init_ui()
        self.init_db()

    def init_ui(self):
        self.setWindowTitle("Registro de Usuario")
        self.setWindowIcon(QIcon("static/icono-ventana.png"))
        self.setGeometry(100, 100, 300, 250)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()
        # Desactiva la redimensión de la ventana 
        self.setFixedSize(300, 200)
        self.name_label = QLabel("Nombre:")
        self.name_input = QLineEdit()
        self.apellido_label = QLabel("Apellido:")
        self.apellido_input = QLineEdit()
        self.username_label = QLabel("Usuario:")
        self.username_input = QLineEdit()
        self.password_label = QLabel("Contraseña:")
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.register_button = QPushButton("Registrar")
        self.register_button.clicked.connect(self.register_user)

        self.layout.addWidget(self.name_label)
        self.layout.addWidget(self.name_input)
        self.layout.addWidget(self.apellido_label)
        self.layout.addWidget(self.apellido_input)
        self.layout.addWidget(self.username_label)
        self.layout.addWidget(self.username_input)
        self.layout.addWidget(self.password_label)
        self.layout.addWidget(self.password_input)
        self.layout.addWidget(self.register_button)

        self.central_widget.setLayout(self.layout)

    def init_db(self):
        try:
            # Cambiar a mysql.connector
            self.db = mysql.connector.connect(
                host='causas.mysql.database.azure.com',
                user='admin_carlos',
                password='F14tomcat',
                database='matias1'
            )

            if self.db.is_connected():
                print("Conexión exitosa a la base de datos MySQL.")
            else:
                print("Error al conectar a la base de datos MySQL.")
                sys.exit(1)

            self.cursor = self.db.cursor()

        except mysql.connector.Error as e:
            print(f"Error al conectar a la base de datos MySQL: {e}")
            sys.exit(1)

    def register_user(self):
        name = self.name_input.text()
        apellido = self.apellido_input.text()
        username = self.username_input.text()
        password = self.password_input.text()

        # Verificar que los campos no estén vacíos
        if not name or not username or not password:
            QMessageBox.warning(self, "Campos Vacíos", "Por favor, complete todos los campos.")
            return

        # Cifrar la contraseña antes de almacenarla
        hashed_password = bcrypt.hash(password)

        # Insertar el nuevo usuario en la base de datos MySQL
        sql = "INSERT INTO usuarios (nombreusuario, apellidousuario, username, password) VALUES (%s, %s, %s, %s)"
        values = (name, apellido, username, hashed_password)

        try:
            self.cursor.execute(sql, values)
            self.db.commit()
            QMessageBox.information(self, "Registro Exitoso", "Usuario registrado correctamente.")
            self.name_input.clear()
            self.apellido_input.clear()
            self.username_input.clear()
            self.password_input.clear()
        except Exception as e:
            print("Error al registrar el usuario:", e)
            self.db.rollback()
            QMessageBox.warning(self, "Error de Registro", "No se pudo registrar el usuario. Inténtalo de nuevo.")

    def close_db_connection(self):
        if self.db.is_connected():
            self.cursor.close()
            self.db.close()

def main():
    app = QApplication(sys.argv)
    register_app = RegisterApp()
    register_app.show()

    # Cierra la conexión de la base de datos cuando se cierra la aplicación
    app.aboutToQuit.connect(register_app.close_db_connection)

    sys.exit(app.exec())

if __name__ == '__main__':
    main()
