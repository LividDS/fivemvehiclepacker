from PyQt6.QtWidgets import QApplication
from gui import MainWindow
import sys

APP_VERSION = "1.0"

app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec())