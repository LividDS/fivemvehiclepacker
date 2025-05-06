import sys

APP_VERSION = "v1.0.1"

try:
    from PyQt6.QtWidgets import QApplication
    from gui.main_window import MainWindow

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

except Exception as e:
    try:
        from PyQt6.QtWidgets import QMessageBox
        msg = QMessageBox()
        msg.setWindowTitle("Startup Error")
        msg.setText(f"The application crashed:\n\n{str(e)}")
        msg.exec()
    except Exception as fallback_error:
        print("❌ FATAL ERROR LAUNCHING APP")
        print("Original exception:", e)
        print("Popup fallback error:", fallback_error)
        input("Press Enter to exit...")
