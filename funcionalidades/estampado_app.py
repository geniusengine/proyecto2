import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget
from docx import Document
from docx2pdf import convert

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
        boton1 = QPushButton('Negativa 52', self)
        boton1.clicked.connect(self.estampar_1)

        boton2 = QPushButton('Negativa Personal', self)
        boton2.clicked.connect(self.estampar_2)

        boton3 = QPushButton('Positivo', self)
        boton3.clicked.connect(self.estampar_3)

        boton4 = QPushButton('Busqueda y Notificacion', self)
        boton4.clicked.connect(self.estampar_4)

        boton5 = QPushButton('Notificacion Personal', self)
        boton5.clicked.connect(self.estampar_5)

        boton6 = QPushButton('Convertir Pdf', self)
        boton6.clicked.connect(self.convertir)

        # Agregar botones al layout vertical
        layout_vertical.addWidget(boton1)
        layout_vertical.addWidget(boton2)
        layout_vertical.addWidget(boton3)
        layout_vertical.addWidget(boton4)
        layout_vertical.addWidget(boton5)

        # Establecer el diseño principal de la ventana
        self.setLayout(layout_vertical)

        # Agregar botones al layout vertical
        layout_vertical.addWidget(boton6)

        # Guardar los datos recibidos
        self.fechaNotificacion = fechaNotificacion
        self.numjui = numjui
        self.nombmandante = nombmandante
        self.nombDemandado = nombDemandado
        self.domicilio = domicilio
        self.rolCausa = rolCausa
        self.arancel = arancel
        self.nombTribunal = nombTribunal

    #1 
    def negativa52(self):
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
        doc.save(f'{self.numjui}.docx')
    
    #2
    def negativaP(self):
        # Crea un nuevo documento de Word
        doc = Document()

        # Agrega el encabezado con los marcadores de posición
        encabezado = f"{self.nombTribunal}\n{self.numjui}: {self.rolCausa}\n{self.nombmandante} CON {self.nombDemandado}"
        doc.add_paragraph(encabezado)

        # Agrega la sección de búsqueda negativa con los datos proporcionados
        busqueda_negativa = f"BÚSQUEDA NEGATIVA: Certifico haber buscado al(la) demandado(a) {self.nombmandante} horas, a fin de notificarle la resolución de fecha {self.fechaNotificacion}. Diligencia que no se llevó a efecto por cuanto el(la) demandado(a) no fue habido(a), {self.rolCausa}. DOY FE."
        doc.add_paragraph(busqueda_negativa)

        # Agrega la firma al final del documento
        doc.add_paragraph(f"Drs. {self.arancel}.-")

        # Guarda el documento
        doc.save(f'{self.numjui}.docx')

    #3
    def positivaP(self):
        # Crea un nuevo documento de Word
        doc = Document()

        # Agrega el encabezado con los marcadores de posición
        encabezado = f"{self.nombTribunal}\n  {self.numjui}: {self.rolCausa}\n  {self.nombmandante} CON {self.nombDemandado}"
        doc.add_paragraph(encabezado)

        # Agrega la sección de búsqueda negativa con los datos proporcionados
        busqueda_positiva = f"BÚSQUEDA POSITIVA:a {self.fechaNotificacion} horas, en su domicilio ubicado en {self.domicilio} busqué a {self.nombDemandado} horas, a fin de notificarle la demanda íntegra y su respectivo proveído, diligencia que no se llevó a efecto por no ser habido en dicho domicilio, en ese momento. Por los dichos de <<constatación1>>.DOY FE.  "
        doc.add_paragraph(busqueda_positiva)

        # Agrega la firma al final del documento
        doc.add_paragraph(f"Drs. {self.arancel}.-")

        # Guarda el documento
        doc.save(f'{self.numjui}.docx')

    #4
    def busquedaN(self):
        # Crea un nuevo documento de Word
        doc = Document()

        # Agrega el encabezado con los marcadores de posición
        encabezado = f"{self.nombTribunal}\n{self.numjui}: {self.rolCausa}\n{self.nombmandante} CON {self.nombDemandado}"
        doc.add_paragraph(encabezado)

        # Agrega la sección de búsqueda negativa con los datos proporcionados
        busquedaN = f"BÚSQUEDA Y NOTIFICACIÓN: a {self.fechaNotificacion} horas, en su domicilio ubicado en {self.domicilio} busqué a {self.nombDemandado}, a fin de notificarle la resolución de fecha <<fecharesolucion52>>, junto al escrito que antecede, diligencia que no se llevó a efecto por no ser habido en dicho domicilio, en ese momento. Informado por <<constatación2>>, quien manifestó que es el domicilio del demandado y que se encuentra en el lugar del juicio, acto seguido procedo a notificar de conformidad al artículo 52 c.p.c. la resolución de fecha <<fecharesolucion52>>, junto al escrito que antecede,  copia integra fue <<constatación2.1>>. DOY FE.  "
        doc.add_paragraph(busquedaN)

        # Agrega la firma al final del documento
        doc.add_paragraph(f"Drs. {self.arancel}.-")

        # Guarda el documento
        doc.save(f'{self.numjui}.docx')

    #5
    def notificacionP(self):
        # Crea un nuevo documento de Word
        doc = Document()

        # Agrega el encabezado con los marcadores de posición
        encabezado = f"{self.nombTribunal}\n{self.numjui}: {self.rolCausa}\n{self.nombmandante} CON {self.nombDemandado}"
        doc.add_paragraph(encabezado)

        # Agrega la sección de búsqueda negativa con los datos proporcionados
        notificacionP = f"NOTIFICACIÓN PERSONAL SUBSIDIARIA: a {self.fechaNotificacion} horas, en su domicilio ubicado en {self.domicilio} busqué a {self.nombDemandado}, se constató que es su domicilio y que se encuentra en el lugar del juicio por <<constatacion-bus/subsi>>, en conformidad al artículo 44 inciso segundo del Código de Procedimiento Civil modificado por el artículo 3, N°3 letra A y B de la ley N°21.394,  la demanda íntegra, su respectivo proveído. Copia íntegra de lo notificado fue <<constatacion-notisubsi>>. Doy fe. "
        doc.add_paragraph(notificacionP)

        # Agrega la firma al final del documento
        doc.add_paragraph(f"Drs. {self.arancel}.-") 

        # Guarda el documento
        doc.save(f'{self.numjui}.docx')

    def pdfxd(self):
        #convertir
        convert(f'{self.numjui}.docx')

        print(f"El archivo PDF se ha creado en: {self.numjui}.pdf")
    

    # Botones enlazados con sus opciones correspindientes    
    def estampar_1(self):
        self.negativa52()

    def estampar_2(self):
        self.negativaP()

    def estampar_3(self):
        self.positivaP()

    def estampar_4(self):
        self.busquedaN()

    def estampar_5(self):
        self.notificacionP()

    def convertir(self):
        self.pdfxd()

def main():
    app = QApplication([])
    ventana = Estampadoxd()
    ventana.show()
    app.exec()

if __name__ == '__main__':
    main()
