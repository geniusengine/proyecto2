import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget
from docx import Document

class Estampadoxd(QMainWindow):
    def __init__(self, fechaNotificacion, numjui, nombmandante, nombDemandado, domicilio, rolCausa, arancel, nombTribunal, parent=None):
        super().__init__(parent)

        self.setWindowTitle('Ventana con Botones')
        self.setGeometry(100, 100, 400, 200)

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        # Layout vertical para organizar los botones
        layout_vertical = QVBoxLayout(self.central_widget)

        # Crear botones
        boton1 = QPushButton('SEXO 1 ?!?!?', self)
        boton1.clicked.connect(self.estampar_1)

        boton2 = QPushButton('SEXO 2 ?!?!?', self)
        boton2.clicked.connect(self.estampar_2)

        boton3 = QPushButton('SEXO 3 ?!?!?', self)
        boton3.clicked.connect(self.estampar_3)

        boton4 = QPushButton('SEXO 4 ?!?!?', self)
        boton4.clicked.connect(self.estampar_4)

        # Agregar botones al layout vertical
        layout_vertical.addWidget(boton1)
        layout_vertical.addWidget(boton2)
        layout_vertical.addWidget(boton3)
        layout_vertical.addWidget(boton4)

        # Guardar los datos recibidos
        self.fechaNotificacion = fechaNotificacion
        self.numjui = numjui
        self.nombmandante = nombmandante
        self.nombDemandado = nombDemandado
        self.domicilio = domicilio
        self.rolCausa = rolCausa
        self.arancel = arancel
        self.nombTribunal = nombTribunal

    # ... (código posterior)

    def llenar_documento(self):
        # Crea un nuevo documento de Word
        doc = Document()

        # Agrega el encabezado con los marcadores de posición
        encabezado = f"{self.nombTribunal}\n{self.numjui}: {self.rolCausa}\n{self.nombmandante} CON {self.nombDemandado}"
        doc.add_paragraph(encabezado)

        # Agrega la sección de búsqueda negativa con los datos proporcionados
        busqueda_negativa = f"BÚSQUEDA NEGATIVA: Certifico haber buscado al(la) demandado(a) {self.nombmandante}, con domicilio en {self.domicilio} especialmente el día {self.fechaNotificacion}, siendo las {self.fechaNotificacion} horas, a fin de notificarle la resolución de fecha {self.fechaNotificacion}. Diligencia que no se llevó a efecto por cuanto el(la) demandado(a) no fue habido(a), {self.rolCausa}. DOY FE."
        doc.add_paragraph(busqueda_negativa)

        # Agrega la firma al final del documento
        doc.add_paragraph(f"Drs. {self.arancel}.-")

        # Guarda el documento
        doc.save('documento_lleno.docx')

    def estampar_1(self):
        self.llenar_documento()

    def estampar_2(self):
        self.llenar_documento()

    def estampar_3(self):
        self.llenar_documento()

    def estampar_4(self):
        self.llenar_documento()

# ... (código posterior)


def main():
    app = QApplication([])
    ventana = Estampadoxd()
    ventana.show()
    app.exec()

if __name__ == '__main__':
    main()
