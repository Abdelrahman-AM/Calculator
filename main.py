import os
import sys
import math
import json
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QGridLayout, QLineEdit, QPushButton, QMessageBox, QDialog, QListWidget
)
from PyQt5.QtCore import Qt
from platformdirs import user_data_dir


class Calculator(QWidget):
    def __init__(self):
        super().__init__()
        self.history_file = self.get_history_file_path()
        self.is_result = False
        self.current_theme = "light"  # Light mode by default
        self.scientific_mode = False  # Basic mode by default
        self.history = self.load_history()
        self.memory = None
        self.init_ui()

    def get_history_file_path(self):
        # Determine the user-specific application directory
        app_data_dir = user_data_dir(appname="Calculator", appauthor="Abdelrahman AM")
        os.makedirs(app_data_dir, exist_ok=True)
        return os.path.join(app_data_dir, "history.json")

    def init_ui(self):
        self.setWindowTitle("Calculator")
        self.setFixedSize(400, 650)  # Set a fixed window size
        self.setWindowFlags(Qt.Window | Qt.WindowMinimizeButtonHint | Qt.WindowCloseButtonHint)  # Disable maximize

        # Main layout
        self.main_layout = QVBoxLayout()
        self.setLayout(self.main_layout)

        # Display
        self.display = QLineEdit()
        self.display.setReadOnly(True)
        self.display.setAlignment(Qt.AlignRight)
        self.display.setStyleSheet("""
            QLineEdit {
                font-size: 28px;
                padding: 10px;
                border: 2px solid #ccc;
                border-radius: 8px;
                background-color: #f5f5f5;
                color: #333;
            }
        """)
        self.main_layout.addWidget(self.display)

        # Button grid
        self.button_grid = QGridLayout()
        self.button_grid.setSpacing(10)
        self.main_layout.addLayout(self.button_grid)

        # Initialize buttons
        self.basic_buttons = [
            "7", "8", "9", "/", "MC",
            "4", "5", "6", "*", "MR",
            "1", "2", "3", "-", "MS",
            "C", "0", "=", "+", "DEL"
        ]
        self.scientific_buttons = [
            "√", "**", "%", ".", "sin(",
            "cos(", "tan(", "log(", "ln(", "π",
            "e", "abs(", "x²", "x³", "1/x"
        ]

        self.extra_buttons = []  # Keep track of scientific buttons
        self.add_buttons(self.basic_buttons)  # Start in basic mode

        # Theme toggle button
        self.theme_button = QPushButton("Toggle Theme")
        self.theme_button.setCursor(Qt.PointingHandCursor)
        self.theme_button.setStyleSheet("""
            QPushButton {
                font-size: 20px;
                background-color: #d0f0d0;
                border: 1px solid #88cc88;
                border-radius: 8px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #b0e0b0;
            }
        """)
        self.theme_button.clicked.connect(self.toggle_theme)
        self.main_layout.addWidget(self.theme_button)

        # History button
        self.history_button = QPushButton("History")
        self.history_button.setCursor(Qt.PointingHandCursor)
        self.history_button.setStyleSheet("""
            QPushButton {
                font-size: 20px;
                background-color: #f0d0d0;
                border: 1px solid #cc8888;
                border-radius: 8px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #e0b0b0;
            }
        """)
        self.history_button.clicked.connect(self.show_history)
        self.main_layout.addWidget(self.history_button)

        # Mode toggle button
        self.toggle_mode_button = QPushButton("Scientific Mode")
        self.toggle_mode_button.setCursor(Qt.PointingHandCursor)
        self.toggle_mode_button.setStyleSheet("""
            QPushButton {
                font-size: 20px;
                background-color: #d0d0f0;
                border: 1px solid #8888cc;
                border-radius: 8px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #b0b0e0;
            }
        """)
        self.toggle_mode_button.clicked.connect(self.toggle_mode)
        self.main_layout.addWidget(self.toggle_mode_button)

    def add_buttons(self, buttons):
        """Add buttons to the grid."""
        row, col = 0, 0
        for button in buttons:
            btn = QPushButton(button)
            btn.setCursor(Qt.PointingHandCursor)
            btn.setStyleSheet("""
                QPushButton {
                    font-size: 18px;
                    background-color: #f0f0f0;
                    border: 1px solid #ccc;
                    border-radius: 8px;
                    padding: 10px;
                }
                QPushButton:hover {
                    background-color: #e0e0e0;
                }
            """)
            btn.clicked.connect(lambda checked, b=button: self.on_button_click(b))
            self.button_grid.addWidget(btn, row, col, 1, 1)
            col += 1
            if col > 4:  # Adjust for 5 columns
                col = 0
                row += 1
            if self.scientific_mode:
                self.extra_buttons.append(btn)

    def toggle_theme(self):
        if self.current_theme == "light":
            self.setStyleSheet("""
                background-color: #2c2c2c;
                color: white;
            """)
            self.display.setStyleSheet("""
                QLineEdit {
                    font-size: 28px;
                    padding: 10px;
                    border: 2px solid #444;
                    border-radius: 8px;
                    background-color: #444;
                    color: white;
                }
            """)
            self.current_theme = "dark"
        else:
            self.setStyleSheet("")
            self.display.setStyleSheet("""
                QLineEdit {
                    font-size: 28px;
                    padding: 10px;
                    border: 2px solid #ccc;
                    border-radius: 8px;
                    background-color: #f5f5f5;
                    color: #333;
                }
            """)
            self.current_theme = "light"

    def toggle_mode(self):
        """Toggle between basic and scientific mode."""
        self.scientific_mode = not self.scientific_mode
        self.clear_buttons()  # Clear the grid
        self.add_buttons(self.basic_buttons)
        if self.scientific_mode:
            self.add_buttons(self.scientific_buttons)
            self.toggle_mode_button.setText("Basic Mode")
        else:
            self.toggle_mode_button.setText("Scientific Mode")

    def clear_buttons(self):
        """Clear all buttons from the grid."""
        while self.button_grid.count():
            item = self.button_grid.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()
        self.extra_buttons = []

    def on_button_click(self, button_value):
        current_text = self.display.text()

        if button_value == "C":
            self.display.clear()
        elif button_value == "DEL":
            self.display.setText(current_text[:-1])
        elif button_value == "=":
            try:
                # Evaluate the expression safely
                result = eval(current_text, {"__builtins__": None}, math.__dict__)
                self.history.append(f"{current_text} = {result}")
                self.save_history()
                self.display.setText(str(result))
            except Exception as e:
                QMessageBox.warning(self, "Error", f"Invalid Input: {e}")
        elif button_value in ["√", "sin(", "cos(", "tan(", "log(", "ln(", "abs("]:
            self.display.setText(current_text + button_value)
        elif button_value == "x²":
            self.display.setText(current_text + "**2")
        elif button_value == "x³":
            self.display.setText(current_text + "**3")
        elif button_value == "1/x":
            self.display.setText(current_text + "1/(")
        elif button_value == "π":
            self.display.setText(current_text + str(math.pi))
        elif button_value == "e":
            self.display.setText(current_text + str(math.e))
        elif button_value == "MC":
            self.memory = None
            QMessageBox.information(self, "Memory Cleared", "Memory has been cleared.")
        elif button_value == "MR":
            if self.memory is not None:
                self.display.setText(str(self.memory))
            else:
                QMessageBox.warning(self, "No Memory", "No value stored in memory.")
        elif button_value == "MS":
            try:
                self.memory = eval(current_text)
                QMessageBox.information(self, "Memory Stored", f"Value {self.memory} stored in memory.")
            except Exception as e:
                QMessageBox.warning(self, "Error", f"Invalid Input: {e}")
        else:
            self.display.setText(current_text + button_value)

    def show_history(self):
        # Create a dialog for displaying history
        history_dialog = QDialog(self)
        history_dialog.setWindowTitle("History")
        history_dialog.setGeometry(200, 200, 300, 400)

        layout = QVBoxLayout()
        history_list = QListWidget()
        history_list.addItems(self.history)
        layout.addWidget(history_list)

        close_button = QPushButton("Close")
        close_button.clicked.connect(history_dialog.accept)
        layout.addWidget(close_button)

        history_dialog.setLayout(layout)
        history_dialog.exec()

    def load_history(self):
        if os.path.exists(self.history_file):
            with open(self.history_file, "r") as f:
                return json.load(f)
        return []

    def save_history(self):
        with open(self.history_file, "w") as f:
            json.dump(self.history, f)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    calculator = Calculator()
    calculator.show()
    sys.exit(app.exec())
