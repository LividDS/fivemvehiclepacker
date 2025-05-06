import os
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton, QSpacerItem, QSizePolicy
)
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QMessageBox
from gui.translator import load_language

class FolderSelectPage(QWidget):
    def __init__(self, language_code='en'):
        super().__init__()
        self.tr = load_language(language_code)
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.setup_ui()

    def setup_ui(self):
        self.layout.setSpacing(10)
        self.layout.setContentsMargins(20, 20, 20, 20)

        self.instruction = QLabel(self.tr["select_mod_instruction"])
        self.instruction.setStyleSheet("font-size: 14pt; font-weight: bold;")
        self.layout.addWidget(self.instruction)

        self.info_label = QLabel(self.tr["mod_instructions"].replace('\\n', '\n'))

        self.info_label.setWordWrap(True)
        self.layout.addWidget(self.info_label)
        self.layout.addSpacing(10)

        self.drag_drop_label = DragDropLabel(self)
        self.layout.addSpacing(10)
        self.layout.addWidget(self.drag_drop_label)
        self.layout.addSpacing(10)

        self.browse_button = QPushButton(self.tr["browse"])
        self.layout.addWidget(self.browse_button)

        self.back_button = QPushButton(self.tr["back"])
        self.layout.addWidget(self.back_button)

        self.layout.addItem(QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))

    def handle_folder_drop(self, folder_path):
        reply = QMessageBox.question(
            self,
            "Confirm Conversion",
            self.tr["confirm_conversion"].format(name=os.path.basename(folder_path)),
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if reply == QMessageBox.StandardButton.Yes:
            self.window().selected_mod_folder = folder_path
            self.instruction.setText(f"{self.tr["select_mod_instruction"]}\n\nSelected folder: {os.path.basename(folder_path)}")
            self.window().run_conversion()


class DragDropLabel(QLabel):
    def __init__(self, parent):
        super().__init__(parent.tr["drag_instruction"])
        self.setAcceptDrops(True)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setStyleSheet("border: 2px dashed #888; padding: 40px;")
        self.parent_ref = parent

    def set_default_style(self, theme):
        if theme == "dark":
            self.setStyleSheet("border: 2px dashed #aaa; color: #aaa; padding: 40px;")
        else:
            self.setStyleSheet("border: 2px dashed #555; color: #555; padding: 40px;")

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event):
        urls = event.mimeData().urls()
        if urls:
            folder_path = urls[0].toLocalFile()
            if os.path.isdir(folder_path):
                self.parent().handle_folder_drop(folder_path)