import os
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton,
    QCheckBox, QSpacerItem, QSizePolicy, QHBoxLayout
)
from PyQt6.QtCore import Qt
from gui.translator import load_language

class WelcomePage(QWidget):
    def __init__(self, language_code='en'):
        super().__init__()
        self.tr = load_language(language_code)
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.setup_ui()

    def setup_ui(self):
        self.layout.setSpacing(15)
        self.layout.setContentsMargins(20, 20, 20, 20)

        self.intro_label = QLabel(self.tr["welcome_title"])
        self.intro_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.intro_label.setStyleSheet("font-size: 20pt; font-weight: bold;")

        self.subtitle_label = QLabel(self.tr["welcome_subtitle"])
        self.subtitle_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.subtitle_label.setWordWrap(True)
        self.subtitle_label.setStyleSheet("font-size: 10pt; font-style: italic; margin-bottom: 10px;")

        self.layout.addWidget(self.intro_label)
        self.layout.addWidget(self.subtitle_label)

        self.output_dir_label = QLabel(self.tr["select_output"])
        self.layout.addWidget(self.output_dir_label)

        output_dir_layout = QHBoxLayout()
        self.output_dir_input = QLineEdit()
        self.output_dir_input.setText(os.getenv("TEMP", "/tmp"))
        self.browse_button = QPushButton(self.tr["browse"])
        output_dir_layout.addWidget(self.output_dir_input)
        output_dir_layout.addWidget(self.browse_button)
        self.layout.addLayout(output_dir_layout)

        self.open_when_done = QCheckBox(self.tr["open_when_done"])
        self.open_when_done.setChecked(True)
        self.layout.addWidget(self.open_when_done)

        self.layout.addItem(QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))

        self.next_button = QPushButton(self.tr["next"])
        self.next_button.setFixedHeight(40)
        self.layout.addWidget(self.next_button)