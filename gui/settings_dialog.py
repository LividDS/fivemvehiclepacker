from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QComboBox, QDialogButtonBox, QFormLayout
)
from PyQt6.QtCore import Qt
from gui.utils import load_settings

class SettingsDialog(QDialog):
    def __init__(self, current_lang='en', parent=None):
        super().__init__(parent)
        self.setWindowTitle("Settings")
        self.setModal(True)
        self.resize(350, 180)

        self.selected_lang = current_lang
        self.settings = load_settings()

        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        form_layout = QFormLayout()
        form_layout.setSpacing(10)

        self.lang_selector = QComboBox()
        self.lang_selector.setStyleSheet("""
        QComboBox {
            background-color: #f0f0f0;
            color: #000000;
            border: 1px solid #ccc;
            border-radius: 4px;
            padding: 4px;
            font-size: 10pt;
        }
        QComboBox::drop-down {
            border-left: 1px solid #ccc;
        }
    """)
        self.lang_selector.addItem("English", userData="en")
        self.lang_selector.addItem("Deutsch", userData="de")
        self.lang_selector.addItem("Français", userData="fr")
        self.lang_selector.addItem("Español", userData="es")
        self.lang_selector.addItem("Português", userData="pt")
        self.lang_selector.addItem("Türkçe", userData="tr")
        self.lang_selector.addItem("Polski", userData="pl")
        self.lang_selector.addItem("Русский", userData="ru")
        self.lang_selector.addItem("简体中文", userData="zh")

        self.lang_selector.setCurrentText(current_lang)
        form_layout.addRow("🌐 Language:", self.lang_selector)

        layout.addLayout(form_layout)

        self.button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)
        layout.addWidget(self.button_box, alignment=Qt.AlignmentFlag.AlignRight)

        self.setLayout(layout)

    def get_selected_language(self):
        return self.lang_selector.currentData()
