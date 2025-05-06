from PyQt6.QtWidgets import QApplication
from gui.main_window import MainWindow
import sys

APP_VERSION = "v1.0.1"

if __name__ == '__main__':
    app = QApplication(sys.argv)

    app.setStyleSheet("""
        QWidget {
            background-color: #ffffff;
            color: #000000;
        }
        QLineEdit {
            background-color: #f0f0f0;
            color: #000000;
            border-radius: 4px;
            padding: 4px;
        }
        QPushButton {
            background-color: #e0e0e0;
            color: #000000;
            border: none;
            padding: 8px;
            border-radius: 6px;
        }
        QPushButton:hover {
            background-color: #3399ff;
            color: white;
        }
        QCheckBox {
            color: #000000;
        }
        QTextEdit {
            background-color: #f0f0f0;
            color: #000000;
        }
    """)

    window = MainWindow()
    window.show()
    sys.exit(app.exec())