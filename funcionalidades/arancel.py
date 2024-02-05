
import sys
from PyQt6.QtWidgets import QDialog, QLabel, QLineEdit, QPushButton, QVBoxLayout, QComboBox, QMessageBox, QApplication

class ActualizarArancelDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Actualizar Arancel")
        self.layout = QVBoxLayout()

        # Create the first QComboBox for letters
        self.combo_letters = QComboBox()
        self.combo_letters.addItems(['A', 'B', 'C', 'D', 'E'])  # Add your letters here
        self.layout.addWidget(self.combo_letters)

        # Create the second QComboBox for numbers
        self.combo_numbers = QComboBox()
        self.layout.addWidget(self.combo_numbers)

        self.btn_actualizar = QPushButton("Aceptar")
        self.btn_actualizar.clicked.connect(self.actualizar_arancel)
        self.layout.addWidget(self.btn_actualizar)

        self.setLayout(self.layout)

        # Connect the signal for changing the letter combo box to update the number combo box
        self.combo_letters.currentIndexChanged.connect(self.update_number_combobox)

    def update_number_combobox(self):
        selected_letter = self.combo_letters.currentText()
        # Update the second combo box based on the selected letter
        self.update_number_combo_box(selected_letter)

    def update_number_combo_box(self, selected_letter):
        # Clear existing items in the number combo box
        self.combo_numbers.clear()

        # Add numbers based on the selected letter
        if selected_letter == 'A':
            self.combo_numbers.addItems(['1', '2', '3'])
        elif selected_letter == 'B':
            self.combo_numbers.addItems(['4', '5', '6'])
        # Add more cases for other letters as needed

    def actualizar_arancel(self):
        # Your existing logic for updating the arancel based on user input
         # Get the selected values from combo boxes
        selected_letter = self.combo_letters.currentText()
        selected_number = self.combo_numbers.currentText()

        # Combine the selected values (you may adjust the format based on your needs)
        new_arancel_value = f"{selected_letter}-{selected_number}"

        # Assume you have access to the table widget in the parent, replace 'table' with your actual table widget
        selected_row = self.parent().table.currentRow()

        # Check if a row is selected
        if selected_row != -1:
            # Update the 'arancel' column in the selected row with the new value
            self.parent().table.setItem(selected_row, 1, QTableWidgetItem(new_arancel_value))

            # You may want to trigger any additional logic here based on the new value

def main():
        app = QApplication(sys.argv)
        window = ActualizarArancelDialog()

        window.show()
        sys.exit(app.exec())

if __name__ == '__main__':
        main()
