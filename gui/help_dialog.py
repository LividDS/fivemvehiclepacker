from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QTextEdit, QDialogButtonBox
from PyQt6.QtCore import Qt

class HelpDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Help Center")
        self.resize(500, 400)

        layout = QVBoxLayout()

        intro = QLabel("How to Use FiveM Vehicle Packer")
        intro.setStyleSheet("font-weight: bold; font-size: 14pt;")
        layout.addWidget(intro)

        help_text = QTextEdit()
        help_text.setReadOnly(True)
        help_text.setPlainText("""\
1. Open the mod's `dlc.rpf` using OpenIV or CodeWalker.
2. Extract all relevant files into a new folder — this includes: `.meta`, `.yft`, `.ytd`, `.ydr`, `.rel`, `.awc`.
3. Select that folder in the tool, then choose an output directory and click Next.
4. The tool will compile and organize the files into a ready-to-use FiveM resource.
5. Use 'Multi-Vehicle Compiler' if you want to combine multiple vehicle mods into a single resource. SOON!
""")

        layout.addWidget(help_text)

        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Close)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

        self.setLayout(layout)