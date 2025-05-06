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
        help_text.setPlainText("""
1. Download the dlc.rpf file from a vehicle of choice and open it in OpenIV or CodeWalker.
2. Create a new folder anywhere, extract any .meta, .yft and .ytd files from the above mentioned dlc.rpf and drop these into your newly created folder.
3. Choose an output directory and click Next.
4. The tool will convert and structure files for FiveM.
5. Use 'Multi-Vehicle Compiler' if you want to combine multiple FiveM asset resources into one FiveM resource.
""")
        layout.addWidget(help_text)

        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Close)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

        self.setLayout(layout)