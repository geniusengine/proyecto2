import sys
import os
from PyQt6.QtWidgets import QApplication, QMainWindow, QFileDialog, QLabel, QPushButton, QVBoxLayout, QWidget
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt
import docx

class WordFileApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Aplicación para Archivos de Word")
        self.setGeometry(100, 100, 800, 600)

        self.initUI()

    def initUI(self):
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()

        self.loadButton = QPushButton("Cargar Archivo Word")
        self.loadButton.clicked.connect(self.loadWordFile)
        self.layout.addWidget(self.loadButton)

        self.fileInfoLabel = QLabel()
        self.layout.addWidget(self.fileInfoLabel)

        self.contentLabel = QLabel()
        self.layout.addWidget(self.contentLabel)
        self.contentLabel.setFixedHeight(400)


        self.stampLabel = QLabel()
        self.layout.addWidget(self.stampLabel)

        self.central_widget.setLayout(self.layout)

        self.file_path = None

    def loadWordFile(self):

        file_path, _ = QFileDialog.getOpenFileName(self, "Abrir archivo de Word", "", "Archivos de Word (*.docx *.doc)")

        if file_path:
            self.file_path = file_path
            self.fileInfoLabel.setText(f"Archivo seleccionado: {os.path.basename(file_path)}")

            # Extraer el contenido del archivo Word
            doc = docx.Document(file_path)
            content = ""
            for paragraph in doc.paragraphs:
                content += paragraph.text + "\n"

            self.contentLabel.setText(content)

            # Agregar el estampado (imagen PNG) en la parte inferior derecha
            stamp = QPixmap("recursos\perra.png")
            self.stampLabel.setPixmap(stamp)
            self.stampLabel.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignBottom)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = WordFileApp()
    window.show()
    sys.exit(app.exec())
