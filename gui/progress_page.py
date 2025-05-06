import os
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QTextEdit, QPushButton,
    QSpacerItem, QSizePolicy, QVBoxLayout
)
from gui.translator import load_language

class ConversionProgressPage(QWidget):
    def __init__(self, language_code='en'):
        super().__init__()
        self.tr = load_language(language_code)
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        self.status_label = QLabel("")
        self.summary_text = QTextEdit()
        self.summary_text.setReadOnly(True)

        self.recent_label = QLabel(self.tr["recent_converted"])
        self.recent_buttons_layout = QVBoxLayout()

        self.done_button = QPushButton(self.tr["done"])
        self.back_button = QPushButton(self.tr["back"])

        layout.addWidget(self.status_label)
        layout.addWidget(self.summary_text)
        layout.addWidget(self.recent_label)
        layout.addLayout(self.recent_buttons_layout)
        layout.addWidget(self.done_button)
        layout.addWidget(self.back_button)
        layout.addItem(QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))

        self.setLayout(layout)

    def update_recent(self, recent_entries):
        for i in reversed(range(self.recent_buttons_layout.count())):
            widget = self.recent_buttons_layout.itemAt(i).widget()
            if widget:
                widget.setParent(None)

        for entry in recent_entries[-5:][::-1]:
            if isinstance(entry, dict):
                path = entry.get("path")
                timestamp = entry.get("timestamp")
            else:
                path = entry
                timestamp = ""
            name = os.path.basename(path)
            btn = QPushButton(f"📂 {name} ({timestamp})" if timestamp else f"📂 {name}")
            from gui.utils import open_folder
            btn.clicked.connect(lambda _, p=path: open_folder(p))
            self.recent_buttons_layout.addWidget(btn)