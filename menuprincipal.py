import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QMessageBox, QInputDialog
from login.login import LoginApp
from login.registro import RegisterApp

class MainMenu(QMainWindow):
    def __init__(self):
        super().__init__()

        # Inicializa la interfaz de usuario
        self.init_ui()

    def init_ui(self):
        # Configura la ventana principal
        self.setWindowTitle("Menú Principal")
        self.setGeometry(100, 100, 300, 200)

        # Configura el widget central y el diseño vertical
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout()

        # Crea y configura los botones
        self.login_button = QPushButton("Iniciar Sesión")
        self.login_button.clicked.connect(self.open_login)
        self.register_button = QPushButton("Registro (Usuario y Contraseña Designados)")
        self.register_button.clicked.connect(self.open_registro)

        # Agrega los botones al diseño
        self.layout.addWidget(self.login_button)
        self.layout.addWidget(self.register_button)

        # Establece el diseño en el widget central
        self.central_widget.setLayout(self.layout)

    def open_login(self):
        # Abre la ventana de inicio de sesión
        self.login_app = LoginApp()
        self.login_app.show()
        
        # Cerrar la ventana de inicio de sesión
        self.close()

    def open_registro(self):
        # Define un usuario y contraseña designados
        usuario_designado = "admin"
        contrasena_designada = "admin"

        # Obtiene usuario y contraseña ingresados por el usuario
        usuario_ingresado, contrasena_ingresada = self.get_usuario_contraseña()

        # Verifica si las credenciales son correctas
        if usuario_ingresado == usuario_designado and contrasena_ingresada == contrasena_designada:
            # Abre la ventana de registro
            self.registro_app = RegisterApp()
            self.registro_app.show()
        else:
            # Muestra un mensaje de error si las credenciales son incorrectas
            msg_box = QMessageBox()
            msg_box.setWindowTitle("Error")
            msg_box.setText("Usuario y/o contraseña incorrectos.")
            msg_box.setIcon(QMessageBox.Icon.Critical)
            msg_box.exec()

    def get_usuario_contraseña(self):
        # Obtiene usuario y contraseña mediante un cuadro de diálogo de entrada
        usuario, ok1 = self.get_input("Ingrese el usuario:")
        contraseña, ok2 = self.get_input("Ingrese la contraseña:")
        return usuario, contraseña

    def get_input(self, prompt):
        # Muestra un cuadro de diálogo de entrada y retorna el texto ingresado
        text, ok = QInputDialog.getText(self, "Entrada", prompt)
        return text, ok

def main():
    # Configura y ejecuta la aplicación
    app = QApplication(sys.argv)
    main_menu = MainMenu()
    main_menu.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
