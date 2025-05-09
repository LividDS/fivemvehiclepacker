import os
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton,
    QFileDialog, QCheckBox, QHBoxLayout, QSpacerItem, QSizePolicy
)
from converter import build_combined_fivem_resource
import webbrowser

class MultiVehicleCompilerPage(QWidget):
    def __init__(self, language_code='en'):
        super().__init__()
        self.language_code = language_code
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.setup_ui()

    def setup_ui(self):
        self.layout.setSpacing(15)
        self.layout.setContentsMargins(20, 20, 20, 20)

        self.title = QLabel("🚗 Multi-Vehicle Resource Compiler")
        self.title.setStyleSheet("font-size: 18pt; font-weight: bold;")
        self.layout.addWidget(self.title)

        self.instructions = QLabel("Drag a folder here or use 'Browse' to select a directory containing multiple vehicle folders.")
        self.instructions.setWordWrap(True)
        self.layout.addWidget(self.instructions)

        self.folder_input = QLineEdit()
        self.folder_input.setPlaceholderText("Drop folder here or click Browse...")
        self.folder_input.setReadOnly(True)
        self.folder_input.setAcceptDrops(True)
        self.folder_input.installEventFilter(self)
        self.layout.addWidget(self.folder_input)

        self.browse_button = QPushButton("📁 Browse Vehicle Folder")
        self.browse_button.clicked.connect(self.browse_folder)
        self.layout.addWidget(self.browse_button)

        self.output_dir_label = QLabel("Select output directory:")
        self.layout.addWidget(self.output_dir_label)

        output_layout = QHBoxLayout()
        self.output_dir_input = QLineEdit()
        self.output_dir_input.setText(os.getenv("TEMP", "/tmp"))
        self.output_browse = QPushButton("📁 Browse")
        self.output_browse.clicked.connect(self.select_output_folder)
        output_layout.addWidget(self.output_dir_input)
        output_layout.addWidget(self.output_browse)
        self.layout.addLayout(output_layout)

        self.open_when_done = QCheckBox("Open output folder when done")
        self.open_when_done.setChecked(True)
        self.layout.addWidget(self.open_when_done)

        self.compile_button = QPushButton("✅ Compile Multi-Vehicle Resource")
        self.compile_button.clicked.connect(self.start_compilation)
        self.layout.addWidget(self.compile_button)

        self.status_label = QLabel("")
        self.status_label.setWordWrap(True)
        self.layout.addWidget(self.status_label)

        self.layout.addItem(QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))

    def browse_folder(self):
        folder_path = QFileDialog.getExistingDirectory(self, "Select Parent Folder Containing Vehicles")
        if folder_path:
            self.folder_input.setText(folder_path)

    def select_output_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Output Folder")
        if folder:
            self.output_dir_input.setText(folder)

    def eventFilter(self, source, event):
        if source == self.folder_input and event.type() == event.Type.DragEnter:
            if event.mimeData().hasUrls():
                event.accept()
                return True
        elif source == self.folder_input and event.type() == event.Type.Drop:
            urls = event.mimeData().urls()
            if urls:
                folder_path = urls[0].toLocalFile()
                if os.path.isdir(folder_path):
                    self.folder_input.setText(folder_path)
                    event.accept()
                    return True
        return super().eventFilter(source, event)

    def start_compilation(self):
        input_path = self.folder_input.text()
        output_path = self.output_dir_input.text()

        if not os.path.isdir(input_path):
            self.status_label.setText("⚠️ Invalid vehicle folder selected.")
            return
        
        final_output = os.path.abspath(os.path.join(output_path, "your_cars_resource"))
        output_folder_name = os.path.basename(final_output)

        vehicle_folders = []
        for name in os.listdir(input_path):
            full_path = os.path.abspath(os.path.join(input_path, name))
            if not os.path.isdir(full_path):
                continue
            if full_path == final_output or os.path.basename(full_path) == output_folder_name:
                continue
            vehicle_folders.append(full_path)

        if not vehicle_folders:
            self.status_label.setText("⚠️ No vehicle folders found in the selected directory.")
            return

        os.makedirs(final_output, exist_ok=True)

        self.status_label.setText("🔄 Compiling multi-vehicle resource...")
        self.repaint()

        try:
            streamed, metas = build_combined_fivem_resource(vehicle_folders, final_output)
            self.status_label.setText(
                f"✅ Done! Output at:\n{final_output}\n\n{len(streamed)} streamed files\n{len(metas)} meta files"
            )

            if self.open_when_done.isChecked():
                webbrowser.open(final_output)
        except Exception as e:
            self.status_label.setText(f"❌ Error: {str(e)}")