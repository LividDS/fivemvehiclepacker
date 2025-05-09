from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QTextEdit, QPushButton,
    QSizePolicy, QSpacerItem
)
from PyQt6.QtGui import QFont
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
        self.summary_text.setFont(QFont("Courier New", 10))
        self.summary_text.setStyleSheet("background-color: black; color: white; border: 1px solid #555;")

        self.done_button = QPushButton(self.tr["done"])
        self.back_button = QPushButton(self.tr["back"])

        layout.addWidget(self.status_label)
        layout.addWidget(self.summary_text)
        layout.addWidget(self.done_button)
        layout.addWidget(self.back_button)
        layout.addItem(QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))

        self.setLayout(layout)

    def show_summary(self, stream_files, meta_files, audio_files):
        summary = "\n✅ Conversion Complete!\n\n"

        if stream_files:
            summary += "📦 Streamed files:\n"
            for f in stream_files:
                summary += f" - {f}\n"

        if meta_files:
            summary += "\n🗂 Meta files:\n"
            for f in meta_files:
                summary += f" - {f}\n"

        if audio_files:
            summary += "\n🔊 Audio files:\n"
            for f in audio_files:
                summary += f" - {f}\n"

        self.summary_text.setPlainText(summary)