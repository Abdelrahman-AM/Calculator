from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QGridLayout, QLineEdit, QPushButton, QMessageBox
)
from PyQt5.QtCore import Qt
import sys
import math


class Calculator(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.is_result = False
        self.current_theme = "light"# Flag to track if the last action was an evaluation
        self.history = []

    def init_ui(self):
        self.setWindowTitle("Calculator")
        self.setGeometry(100, 100, 400, 500)

        # Main layout
        main_layout = QVBoxLayout()
        self.setLayout(main_layout)

        # Display
        self.display = QLineEdit()
        self.display.setReadOnly(True)
        self.display.setAlignment(Qt.AlignRight)
        self.display.setStyleSheet("font-size: 24px;")
        main_layout.addWidget(self.display)

        theme_button = QPushButton("Theme")
        theme_button.setStyleSheet("font-size: 18px; padding: 10px;")
        theme_button.clicked.connect(self.toggle_theme)
        main_layout.addWidget(theme_button)

        # Button grid
        button_grid = QGridLayout()
        main_layout.addLayout(button_grid)

        # Button layout
        buttons = [
            "7", "8", "9", "/",
            "4", "5", "6", "*",
            "1", "2", "3", "-",
            "C", "0", "=", "+",
            "√", "**", "%", ".",
            "DEL", "sin(x)"
        ]

        # Add buttons to the grid
        row, col = 0, 0
        for button in buttons:
            btn = QPushButton(button)
            btn.setStyleSheet("font-size: 18px; padding: 10px;")
            btn.clicked.connect(lambda checked, b=button: self.on_button_click(b))
            button_grid.addWidget(btn, row, col, 1, 1 if button != "DEL" else 2)  # Make "DEL" span 2 columns
            col += 1 if button != "DEL" else 2
            if col > 3:
                col = 0
                row += 1

    def toggle_theme(self):
        if self.current_theme == "light":
            self.setStyleSheet("background-color: #2c2c2c; color: white;")
            self.display.setStyleSheet("font-size: 24px; colour: white")
            self.current_theme = "dark"

        else:
            self.setStyleSheet("")
            self.display.setStyleSheet("font-size: 24px; colour: black")
            self.current_theme = "light"

    def on_button_click(self, button_value):
        current_text = self.display.text()

        # Clear the display if the last action was an evaluation and a number is pressed
        if self.is_result and button_value.isdigit():
            current_text = ""
            self.is_result = False

        if button_value == "C":
            self.display.clear()
            self.is_result = False
        elif button_value == "DEL":
            self.display.setText(current_text[:-1])
        elif button_value == "=":
            try:
                result = eval(current_text)
                self.history.append(f"{current_text} = {result}")
                self.display.setText(str(result))
                self.is_result = True  # Set flag to indicate result has been shown
            except Exception as e:
                QMessageBox.warning(self, "Error", f"Invalid Input: {e}")
                self.is_result = False
        elif button_value == "√":
            try:
                result = eval(current_text)
                if result < 0:
                    raise ValueError("Cannot calculate the square root of a negative number")
                self.display.setText(str(math.sqrt(result)))
                self.is_result = True  # Set flag to indicate result has been shown
            except Exception as e:
                QMessageBox.warning(self, "Error", f"Invalid Input: {e}")
                self.is_result = False
        elif button_value == "sin(x)":
            try:
                result = math.sin(math.radians(eval(current_text)))
                self.display.setText(str(result))
                self.is_result = True
            except Exception as e:
                QMessageBox.warning(self, "Error", f"Invalid Input: {e}")
        else:
            self.display.setText(current_text + button_value)
            self.is_result = False  # Reset flag for all other actions


if __name__ == "__main__":
    app = QApplication(sys.argv)
    calculator = Calculator()
    calculator.show()
    sys.exit(app.exec())
