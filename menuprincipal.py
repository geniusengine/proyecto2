import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QMessageBox, QInputDialog
from login import LoginApp
from formularios.registro import RegisterApp

class MainMenu(QMainWindow):
    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Menú Principal")
        self.setGeometry(100, 100, 300, 200)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()

        self.login_button = QPushButton("Iniciar Sesión")
        self.login_button.clicked.connect(self.open_login)
        self.register_button = QPushButton("Registro (Usuario y Contraseña Designados)")
        self.register_button.clicked.connect(self.open_registro)

        self.layout.addWidget(self.login_button)
        self.layout.addWidget(self.register_button)

        self.central_widget.setLayout(self.layout)

    def open_login(self):
        self.login_app = LoginApp()
        self.login_app.show()

    def open_registro(self):
        usuario_designado = "RobertoNarigon"
        contrasena_designada = "tulachi"

        usuario_ingresado, contrasena_ingresada = self.get_usuario_contraseña()

        if usuario_ingresado == usuario_designado and contrasena_ingresada == contrasena_designada:
            self.registro_app = RegisterApp()
            self.registro_app.show()
        else:
            msg_box = QMessageBox()
            msg_box.setWindowTitle("Error")
            msg_box.setText("Usuario y/o contraseña incorrectos.")
            msg_box.setIcon(QMessageBox.Icon.Critical)
            msg_box.exec()

    def get_usuario_contraseña(self):
        usuario, ok1 = self.get_input("Ingrese el usuario:")
        contraseña, ok2 = self.get_input("Ingrese la contraseña:")
        return usuario, contraseña

    def get_input(self, prompt):
        text, ok = QInputDialog.getText(self, "Entrada", prompt)
        return text, ok

def main():
    app = QApplication(sys.argv)
    main_menu = MainMenu()
    main_menu.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
